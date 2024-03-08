"""api_client.SearchAPIClient tests"""
import requests_mock
from api_client import SearchAPIClient


def test_store_method_successful():
    """Mocks the api client store post method success call"""
    client = SearchAPIClient()
    mock_result = {"data": {"key": "key", "body": "body"}}
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(method="POST",
                            url=client.base_url+"/store",
                            status_code=200,
                            json=mock_result,)
        result = client.store(
            mock_result["data"]["body"])
        assert result == mock_result


def test_store_method_error():
    """Mocks the api client store post method error"""
    client = SearchAPIClient()
    mock_result = {"key": "key", "body": "body"}
    with requests_mock.Mocker() as mocker:
        mocker.register_uri(method="POST",
                            url=client.base_url+"/store",
                            status_code=400,
                            json=mock_result,)
        result = client.store(
            mock_result["body"])
        assert "error" in result
