"""Encapsulates Downstream Search Rest API calls"""
import logging
import requests
from conf.config import Configuration

class SearchAPIClient:
    """CXGenius Search Rest API Client"""
    conf = Configuration()
    logger = logging.getLogger(__name__)

    def store(self, documents):
        """Store all the doc collection"""
        success = 0
        failure = 0
        for doc in documents:
            r = self.store_one(doc)
            if "error" in r:
                failure+=1
            else:
                success+=1
                self.logger.debug("Successfully pushed %s", doc["key"])
        return {"success": success, "failure":failure}

    def store_one(self, document_body):
        """POST request to /store endpoint"""
        headers = {
            "X-API-KEY": self.conf.http_client_api_key
        }
        data = document_body
        try:
            response = requests.post(f"{self.conf.base_url}/api/store", json=data,
                                     headers=headers, timeout=self.conf.http_client_timeout)
            response.raise_for_status()

            return response.json()
        except requests.Timeout:
            self.logger.warning("Request timed out")
            return {"error": "The request timed out"}
        except requests.RequestException as error:
            self.logger.warning("An error occured: %s", error)
            return {"error": f"An error occured: {error}"}
