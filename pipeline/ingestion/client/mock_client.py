"""CXGenius Mock Client"""
import logging

logger = logging.getLogger(__name__)

class SearchMockClient:
    """CXGenius Mock Client for local tests"""
    def store(self, documents):
        """CXGenius Mock store for local tests"""
        for doc in documents:
            logger.debug("Mock store %s\n%s\n\n", doc["key"], doc)
        return {"success": len(documents), "failure":0}
