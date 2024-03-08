"""CXGenius Search main ingestion script"""
import argparse
import logging
from ingestion.jira_ingestion import JiraIngestion
from ingestion.public_docs_ingestion import PubDocumentIngestion
from ingestion.salesforce_ingestion import SalesforceIngestion
from ingestion.knowledge_articles_ingestion import KBIngestion
from common.execution_time_tracker import ExecutionTimeTracker
from conf.config import Configuration

conf = Configuration()

# Configure logging settings
logging.basicConfig(level=conf.log_level,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('ingestion.log'),
                                logging.StreamHandler()])
logger = logging.getLogger(__name__)

sources = ["jira","documents", "cases", "kbs"]

def start_ingestion():
    """Starts ingestion"""
    global sources
    parser = argparse.ArgumentParser(description='Ingestion client arguments.')
    
    parser.add_argument('--sources',
                        type=str,
                        help=f'Specify one or more comma-separated sources to use, if not passing any, by default all ({",".join(sources)}) are ingested')
    parser.add_argument('--deduplication',
                        action='store_true',
                        help='Deduplicate documents')
    parser.add_argument('--salesforce_limit',
                        type=str,
                        help='Specify a limit for the max cases to get from Salesforce on a single ingestion')    
    # Parse the arguments
    args = parser.parse_args()

    # Logic based on the arguments
    if args.sources:
        sources = args.sources.split(",")
    logger.info("Using %s sources", sources)

    deduplication = args.deduplication
    salesforce_limit = None
    if args.salesforce_limit:
        salesforce_limit = args.salesforce_limit
    ingestion = None
    if "jira" in sources:
        # Ingest from JIRA
        logger.info("Start JIRA Ingestion")
        time_tracker = ExecutionTimeTracker(
            file_path='cxgenius_search/last_jira_ingestion_ts.log')
        ingestion = JiraIngestion(time_tracker=time_tracker)
    if "documents" in sources:
        # Ingest from Cloudera Public Documentation
        logger.info("Start Public Doc Ingestion")
        ingestion = PubDocumentIngestion(options={"deduplication": deduplication})
    if "cases" in sources:
        # Ingest from Salesforce
        logger.info("Start Salesforce Ingestion")
        time_tracker = ExecutionTimeTracker(
            file_path='cxgenius_search/last_cases_ingestion_ts.log')
        ingestion = SalesforceIngestion(time_tracker=time_tracker, options={"salesforce_limit": salesforce_limit})
    if "kbs" in sources:
        # Ingest from KBs
        logger.info("Start KB article Ingestion")
        time_tracker = ExecutionTimeTracker(
            file_path='cxgenius_search/last_kbs_ingestion_ts.log')
        ingestion = KBIngestion(time_tracker=time_tracker, options={})
    if ingestion:
        ingestion.ingest()
    else:
        logger.error("No source selected!")

if __name__ == "__main__":
    start_ingestion()
