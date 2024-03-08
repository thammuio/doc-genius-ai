"""Downstream Client Factory"""
from ingestion.client.api_client import SearchAPIClient
from ingestion.client.kafka_client import KafkaClient
from ingestion.client.mock_client import SearchMockClient
from conf.config import Configuration

conf = Configuration()

def get_client(key=conf.default_downstream_client):
    """Client Factory Method"""
    clients = {
        "SearchAPIClient": SearchAPIClient,
        "KafkaClient": KafkaClient,
        "SearchMockClient": SearchMockClient,
    }
    return clients[key]()
