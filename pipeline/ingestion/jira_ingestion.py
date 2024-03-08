"""CXGenius Search JIRA ingestion script """
from datetime import datetime
import logging
from jira import JIRA

from ingestion.downstream_client import get_client
from conf.config import Configuration
from marshmallow import ValidationError
from entities.document import DocumentSchema, ScrapSchema
from dateutil import parser


logger = logging.getLogger(__name__)

JIRA_PROJECTS = [
    "Backline Escalations",
    "Engineering Escalations",
    "CDP Distro",
    "Cloudera Manager (CM)",
    "TSB", 
    "Cloudera Machine Learning",
    "Data Engineering Experience",
    "Data Warehouse  eXperience",
    "CFM",
    "Cloudera Streaming Analytics",
    "Compute Platform",
    "PULSE",
    "Key Trustee",
    "Cloudbreak",
    "SaaS Engineering"]

class JiraClient:
    """Encapsulates Jira client"""
    conf = Configuration()

    jira = JIRA('https://jira.cloudera.com',
                token_auth=conf.jira_token_auth)

    def search_issues(self, query, start_at, fields, max_results=99999):
        """Searches jira issues"""
        return self.jira.search_issues(query, startAt=start_at,
                                       fields=fields,
                                       maxResults=max_results)


class JiraIngestion:
    """Jira ingestion"""

    def __init__(self, time_tracker=None, client=JiraClient()):
        self.time_tracker = time_tracker
        self.client = client

    def get_components(self, row, max_items=10, max_len=100):
        """Extract list of components from jira document"""
        comp_list = []
        if not row.raw["fields"].get("customfield_12419") is None:
            comp_list.append(row.fields.customfield_12419)

        # limit to 10 components and also length <=100
        for i in row.fields.components:
            if len(comp_list) > max_items or len(", ".join(comp_list)) > max_len:
                break
            comp_list.append(i.name)

        return list(set(comp_list))

    def get_versions(self, row, max_items=10, max_len=100):
        """Extract list of versions from jira document"""
        version_list = []
        # limit to 10 versions and also length <=100
        if hasattr(row.fields, 'versions'):
            for i in row.fields.versions:
                if len(version_list) > max_items or len(", ".join(version_list)) > max_len:
                    break
                version_list.append(i.name)
        if len(version_list)==0:
                if not row.raw["fields"].get("customfield_12413") is None:
                    version_list.append(row.fields.customfield_12413)
        return list(set(version_list))

    def get_assignee(self, row):
        """Extract assignee from jira document"""
        if row.fields.assignee and row.fields.assignee.emailAddress:
            return row.fields.assignee.emailAddress
        return ''

    def get_created_at(self, row):
        """Extract created data from jira document"""
        if row.fields.created:
            return row.fields.created
        return ''

    def get_updated_at(self, row):
        """Extract last updated date from jira document"""
        if row.fields.updated:
            return row.fields.updated
        return ''

    def fetch_documents(self, last_execution_time=''):
        """Fetch from Jira and return a jira document array"""
        projects = '","'.join(JIRA_PROJECTS)
        query = f'project in ("{ projects }")'
        #query += 'and type in (Escalation, Bug, "Enhancement Request", Improvement)'
        if last_execution_time:
            # filter push down to fetch only what has changed since last execution datetime
            query += f' and updated > "{last_execution_time}"'
        query += ' ORDER BY key ASC'

        fields = ["assignee", "components", "summary", "description", "created", "updated",
                  "customfield_16432", "customfield_16433", "customfield_15944", "versions",
                  "customfield_12311", "customfield_11412", "customfield_16413",
                  "customfield_12419", "customfield_16611", "customfield_16434",
                  "customfield_18210", "customfield_12413", "comment"]

        # problem statement = customfield_16432
        # frontline analysis = customfield_16433 | customfield_15944
        # action needed = customfield_16434 | customfield_18210
        # csh account_name | customer name  = customfield_12311 | customfield_11412
        # csh product = customfield_16413
        # csh component = customfield_12419
        # csh experience = customfield_16611
        # csh product version = customfield_12413

        logger.info("FetchDocuments from Jira")

        documents = []  # jira results
        start_at = 0
        total = 99999

        while start_at < total:
            rows = self.client.search_issues(
                query, start_at=start_at, fields=fields)
            total = rows.total
            num_rows = 0
            for row in rows:
                num_rows += 1
                key = row.key
                comp_list = self.get_components(row)
                version_list = self.get_versions(row)
                assignee = self.get_assignee(row)
                created_at = parser.parse(self.get_created_at(row)).isoformat()
                updated_at = parser.parse(self.get_updated_at(row)).isoformat()
                account_name = ''
                if not row.raw["fields"].get("customfield_12311") is None:
                    account_name = row.fields.customfield_12311
                elif not row.raw["fields"].get("customfield_11412") is None:
                    account_name = row.fields.customfield_11412

                product_name = []
                if not row.raw["fields"].get("customfield_16413") is None:
                    product_name = row.fields.customfield_16413.split(',')

                experience_name = ''
                if not row.raw["fields"].get("customfield_16611") is None:
                    experience_name = row.fields.customfield_16611

                text_corpus = str(row.raw["fields"].get("customfield_16432") or '') + "\n"
                text_corpus += str(row.raw["fields"].get("customfield_16433") or
                                   row.raw["fields"].get("customfield_15944") or '') + "\n"
                text_corpus += str(row.raw["fields"].get("customfield_16434") or
                                   row.raw["fields"].get("customfield_18210") or '')
                                   
                scraps = []
                title_description = {
                    "doc_id": key,
                    "type_name": "title_description",
                    "scrap_text": row.fields.summary + "\n" + str(row.fields.description or ''),
                    "posted_by": assignee,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
                cdm = {
                    "doc_id": key,
                    "type_name": "problem_analysis_action",
                    "scrap_text": text_corpus,
                    "posted_by": assignee,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
                scraps.append(title_description)
                scraps.append(cdm)

                if row.fields.comment and row.fields.comment.comments:
                    for c in row.fields.comment.comments:
                        author = ''
                        if c.author.emailAddress:
                            author = c.author.emailAddress

                        scrap_text = c.body

                        scrap_created = parser.parse(c.created).isoformat()
                        scrap_updated = parser.parse(c.updated).isoformat()

                        scrap = {
                            "doc_id": key,
                            "type_name": "comment",
                            "scrap_text": scrap_text,
                            "posted_by": author,
                            "created_at": scrap_created,
                            "updated_at": scrap_updated
                        }
                        scraps.append(scrap)

                doc = DocumentSchema().load({
                    "id": key,
                    "ref_id": key,
                    "type_name": "tsb" if key.startswith('TSB-') else "jira",
                    "owner_email": assignee,
                    "account_name": account_name,
                    "component": [*set(comp_list)],
                    "product_name": [*set(product_name)],
                    "experience_name": experience_name,
                    "crv": version_list,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "scraps": scraps
                })
                logger.debug("Adding Jira: %s", key)
                logger.debug(doc)

                documents.append(doc)

            start_at = start_at + num_rows
            logger.info("curr/total %d/%d", start_at, total)

        logger.info(
            "Total # of Jiras documents to be processed: %d", len(documents))
        return documents

    def push(self, docs):
        """Pushes docs downstream using client"""
        logger.info("Pushing documents downstream")
        client = get_client()
        r = client.store(docs)

        logger.info(
            "Successfully pushed a total of %d documents downstream", r["success"])
        logger.info("Failed to push a total of %d documents", r["failure"])

    def ingest(self):
        """Fetches docs from jira and pushes to downstream"""
        last_execution_time = self.get_last_execution_datetime()
        now = datetime.now()
        docs = self.fetch_documents(last_execution_time)
        self.push(docs)
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
