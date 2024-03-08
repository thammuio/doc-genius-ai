"""CXGenius Search KB article ingestion script """
from datetime import datetime
import logging
import pprint
import sqlite3
from html import unescape
from bs4 import BeautifulSoup
from dateutil import parser
from ingestion.downstream_client import get_client
from conf.config import Configuration
from entities.document import DocumentSchema, ScrapSchema
import common.components as comp

class KBIngestion:
    
    conf = Configuration()
    logger = logging.getLogger(__name__)
    pp = pprint.PrettyPrinter(indent=4)

    def __init__(self, time_tracker=None, options=None):
        self.time_tracker = time_tracker
        self.options = options
        self.conn = sqlite3.connect("KBs.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    

    def fetchDivContentByClassName(self, rawHTML, className):
        self.logger.debug("fetchDivContentByClassName(%s, %s)", rawHTML, className)
        content = rawHTML
        soup = BeautifulSoup(str(content), "lxml")
        divs = soup.find_all("div", {'class':className})
        output = []
        for div in divs:    
            if div.h2:
                div.h2.decompose()
            r = self.cleanText(div.text)
            if r and len(r)>10:
                output.append(r)
        self.logger.debug("fetchDivContentByClassName returned: %s", ", ".join(output))
        return output

    def cleanText(self, html):
        html = unescape(html)
        elem = BeautifulSoup(html, "lxml")
        text = ''
        for e in elem.descendants:
            if isinstance(e, str):
                text += e.strip()
            elif e.name == 'br' or e.name == 'p':
                text += '\n'
        return text.replace("\xa0", " ")
    
    def fetch_documents(self, last_execution_time=''):
        """Fetch from the KB and return a document array"""

        self.logger.info("FetchDocuments from KB articles")
        
        # Get KBs
        query = "SELECT kb_id, last_edit_dt, first_publish_dt, author_email, component_labels, product_labels, subject, summary, body FROM kbs WHERE board != 'archive' AND is_inreview IS FALSE"
        
        if last_execution_time:
            # filter push down to fetch only what has changed since last execution datetime
            query += f' AND last_edit_dt > "{parser.parse(last_execution_time).strftime("%Y-%m-%d %H:%M:%s.%f")}"'

        results = self.cursor.execute(query)
        docs = []
        for kb in results.fetchall():
            assignee = "unassigned"
            if kb["author_email"]:
                assignee = kb["author_email"]
            kb_created = datetime.now().isoformat()
            if kb["first_publish_dt"]:
                kb_created = parser.parse(kb["first_publish_dt"]).isoformat()
            kb_updated = kb_created
            if kb["last_edit_dt"]:
                kb_updated = parser.parse(kb["last_edit_dt"]).isoformat()
            
            product_name = str(kb["product_labels"] or "")
            
            scraps = []

            subject = kb["subject"]
            summary = kb["summary"]
            if summary:
                summary = " ".join(self.fetchDivContentByClassName(summary, "summary"))
            else:
                summary = " ".join(self.fetchDivContentByClassName(kb["body"], "summary"))

            raw_text = ""

            # infer component and product from applies and labels
            applies_to = self.fetchDivContentByClassName(kb["body"], "applies")
            comp_list = comp.findComponentsIn(" ".join(applies_to))
            if product_name:
                comp_list = comp_list + comp.findComponentsIn(product_name)
            if kb["component_labels"]:
                comp_list = comp_list + comp.findComponentsIn(kb["component_labels"])

            for c in ["symptoms", "cause"]:
                ct = self.fetchDivContentByClassName(kb["body"], c)
                raw_text = raw_text + " ".join(ct)

            kb_id = "kb_" + kb["kb_id"]
            if subject or summary:
                scrap = ScrapSchema().load({
                        "doc_id": kb_id,
                        "type_name": "title_description",
                        "scrap_text": (subject or  "") + "\n" + (summary or ""),
                        "created_at": kb_created,
                        "updated_at": kb_updated
                    })
                scraps.append(scrap)

            if raw_text:
                scrap = ScrapSchema().load({
                        "doc_id": kb_id,
                        "type_name": "problem_analysis_action",
                        "scrap_text": raw_text,
                        "posted_by": assignee,
                        "created_at": kb_created,
                        "updated_at": kb_updated
                    })
                scraps.append(scrap)

            kb_body = self.cleanText(kb["body"])
            if len(kb_body) > 0:
                scrap = ScrapSchema().load({
                        "doc_id": kb_id,
                        "type_name": "body_comment",
                        "scrap_text": kb_body,
                        "posted_by": assignee,
                        "created_at": kb_created,
                        "updated_at": kb_updated
                    })
                scraps.append(scrap)

            doc = DocumentSchema().load({
                "id": kb_id,
                "ref_id": kb["kb_id"],
                "type_name": "kb",
                "owner_email": assignee,
                "component": [*set(comp_list)],
                "product_name": [*set(product_name.split(','))],
                "created_at": kb_created,
                "updated_at": kb_updated,
                "scraps": scraps
            })
            #self.pp.pprint(doc)
            docs.append(doc)

        self.logger.info(
            "Total # of KBs to be processed: %d", len(docs))
        return docs

    def push(self, docs):
        """Pushes kbs downstream using client"""
        self.logger.info("Pushing %d KBs", len(docs))
        client = get_client()
        r = client.store(docs)

        self.logger.info(
            "Successfully pushed a total of %d documents downstream", r["success"])
        self.logger.info("Failed to push a total of %d documents", r["failure"])

    def ingest(self):
        """Fetches KB articles and pushes to downstream"""
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


