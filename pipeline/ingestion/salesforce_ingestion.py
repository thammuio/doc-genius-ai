"""CXGenius Search Salesforce ingestion script """
from datetime import datetime
import logging
import pprint
from simple_salesforce import Salesforce
import re
from ingestion.downstream_client import get_client
from conf.config import Configuration
from marshmallow import ValidationError
from entities.document import DocumentSchema, ScrapSchema
from dateutil import parser




class SalesforceIngestion:
    
    conf = Configuration()
    logger = logging.getLogger(__name__)
    pp = pprint.PrettyPrinter(indent=4)
    sf = None
    beginning_id = re.compile(r"^[0-9a-z-A-Z]{18}\n?")

    def __init__(self, time_tracker=None, options=None):
        self.time_tracker = time_tracker
        self.options = options
        if self.conf.is_production:
            self.sf = Salesforce(username=self.conf.salesforce_config["username"], password=self.conf.salesforce_config["password"],
                                security_token=self.conf.salesforce_config["token"])
        else:
            self.sf = Salesforce(username=self.conf.salesforce_config["username"], password=self.conf.salesforce_config["password"],
                                security_token=self.conf.salesforce_config["token"], domain=self.conf.salesforce_config["domain"])
           
    
    def fetch_documents(self, last_execution_time=''):
        """Fetch from the Salesforce and return a document array"""

        self.logger.info("FetchDocuments from Salesforce")
        
        # Get cases NOTE that cdp_Issue_customer__c is not available on prod currently, so it was removed from the query at this moment
        query = "SELECT Id, CaseNumber, Case.Owner.Email, Case.Account.Name, Description, Subject, cdp_Answer__c, cdp_Cause__c, \
            cdp_Customer_Action_plan__c, cdp_Issue__c, cdp_Question__c, cdp_Solution__c, Pillar__c, Component__c, \
            Product_Type__c, Experience__c, Runtime_Version_at_Case_Creation__c, CM_Version__c, CreatedDate, LastModifiedDate, \
                (select CommentBody, IsPublished, CaseComment.CreatedBy.Email, CreatedDate, LastModifiedDate from CaseComments where IsDeleted = FALSE) \
                    FROM Case WHERE Status in ('Solved', 'Pending Future Release', 'Cloudera Researching', 'Awaiting Customer Response', 'Customer Responded', 'Solution Proposed')"
        # for limiting ingestion to be from a certain ts:
        # AND CreatedDate > 2020-01-01T00:00:00Z"
        
        if last_execution_time:
            # filter push down to fetch only what has changed since last execution datetime
            query += f' AND LastModifiedDate > {parser.parse(last_execution_time).strftime("%Y-%m-%dT%H:%M:%SZ")}'
        if self.options.get("salesforce_limit"):
            query += " limit " + str(self.options.get("salesforce_limit"))
        fetch_results = self.sf.bulk.Case.query(query,lazy_operation = True)
        case_batch = 0
        total_docs = 0
        for list_results in fetch_results:
            case_batch += 1
            docs = []
            self.logger.info("Got cases batch #%d that had %d cases",case_batch, len(list_results))
            for case in list_results:
                # Iterate getting comments for each case
                # query_response = self.sf.query_all(f"select CommentBody, IsPublished, CaseComment.CreatedBy.Email, CreatedDate, LastModifiedDate from CaseComment where ParentId = '{case['Id']}' and IsDeleted = FALSE")
                scraps = []
                if case.get("CaseComments"):
                    for comment in case["CaseComments"]["records"]:
                        poster = ""
                        if comment.get("CreatedBy") and comment["CreatedBy"].get("Email"):
                            poster = comment["CreatedBy"]["Email"]
                        comment_body = comment.get("CommentBody") or ""
                        comment_body = self.beginning_id.sub('', comment_body)
                        scrap = ScrapSchema().load({
                                "doc_id": case["CaseNumber"],
                                "type_name": "public_comment" if comment["IsPublished"] else "private_comment",
                                "scrap_text": comment_body,
                                "posted_by": poster,
                                "created_at": datetime.fromtimestamp(int(comment["CreatedDate"]/1000)).isoformat(),
                                "updated_at": datetime.fromtimestamp(int(comment["LastModifiedDate"]/1000)).isoformat()
                            })
                        scraps.append(scrap)
                assignee = "unassigned"
                if case.get("Owner") and case["Owner"].get("Email"):
                    assignee = case["Owner"]["Email"]
                account_name = ""
                if case.get("Account") and case["Account"].get("Name"):
                    account_name = case["Account"]["Name"]
                # CDM
                case_created = datetime.fromtimestamp(int(case["CreatedDate"]/1000)).isoformat()
                case_updated = datetime.fromtimestamp(int(case["LastModifiedDate"]/1000)).isoformat()
                
                components = []
                if case.get("Component__c"):
                    components.append(case.get("Component__c"))
                versions = []
                if case.get("Runtime_Version_at_Case_Creation__c"):
                    versions.append(case.get("Runtime_Version_at_Case_Creation__c"))
                
                product_name = str(case.get("Product_Type__c") or "")
                
                if case.get("Description") or case.get("Subject"):
                    scrap = ScrapSchema().load({
                            "doc_id": case["CaseNumber"],
                            "type_name": "title_description",
                            "scrap_text":   (case.get("Subject") or  "") + "\n" + (case.get("Description") or ""),
                            "posted_by": assignee,
                            "created_at": case_created,
                            "updated_at": case_updated
                        })
                    scraps.append(scrap)
                if case.get("cdp_Issue_customer__c") or case.get("cdp_Cause__c") or case.get("cdp_Customer_Action_plan__c") or case.get("cdp_Issue__c") or case.get("cdp_Question__c"):
                    scrap = ScrapSchema().load({
                            "doc_id": case["CaseNumber"],
                            "type_name": "problem_analysis_action",
                            "scrap_text": (case.get("cdp_Issue_customer__c") or "") + "\n" + (case.get("cdp_Issue__c") or "") + "\n" + 
                                            (case.get("cdp_Cause__c") or "") + "\n" + (case.get("cdp_Customer_Action_plan__c") or "") + "\n"+ 
                                            (case.get("cdp_Question__c") or ""),
                            "posted_by": assignee,
                            "created_at": case_created,
                            "updated_at": case_updated
                        })
                    scraps.append(scrap)
                if case.get("cdp_Solution__c") or case.get("cdp_Answer__c"):
                    scrap = ScrapSchema().load({
                            "doc_id": case["CaseNumber"],
                            "type_name": "answer_solution_comment",
                            "scrap_text": (case.get("cdp_Answer__c") or "") + "\n" + (case.get("cdp_Solution__c") or ""),
                            "posted_by": assignee,
                            "created_at": case_created,
                            "updated_at": case_updated
                        })
                    scraps.append(scrap)

                cm_versions = []
                if case.get("CM_Version__c"):
                    cm_versions.append(case.get("CM_Version__c"))
                doc = DocumentSchema().load({
                    "id": case["CaseNumber"],
                    "ref_id": case["Id"],
                    "type_name": "cases",
                    "owner_email": assignee,
                    "pillar_name": (case.get("Pillar__c") or ""),
                    "account_name": account_name,
                    "component": components,
                    "product_name":  [*set(product_name.split(','))],
                    "experience_name": (case.get("Experience__c") or ""),
                    "crv": versions,
                    "cmv": cm_versions,
                    "created_at": case_created,
                    "updated_at": case_updated,
                    "scraps": scraps
                })
                docs.append(doc)
            to_push = len(docs)
            total_docs += to_push

            self.push(docs)

        self.logger.info(
            "Total # of cases to be processed: %d", total_docs)
        return

    def push(self, docs):
        """Pushes docs downstream using client"""
        self.logger.info("Pushing %d cases", len(docs))
        client = get_client()
        r = client.store(docs)

        self.logger.info(
            "Successfully pushed a total of %d documents downstream", r["success"])
        self.logger.info("Failed to push a total of %d documents", r["failure"])

    def ingest(self):
        """Fetches cases from Salesforce and pushes to downstream"""
        last_execution_time = self.get_last_execution_datetime()
        now = datetime.now()
        self.fetch_documents(last_execution_time)
        
        self.record_datetime(now)

    def get_last_execution_datetime(self):
        """Reads the last execution datetime"""
        if self.time_tracker:
            return str(self.time_tracker.get_last_execution_datetime())
        return ''

    def record_datetime(self, dt):
        """Stores the datetime"""
        if self.time_tracker:
            self.time_tracker.record_current_datetime(dt=dt)


