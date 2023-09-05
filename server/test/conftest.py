import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="module")
def base_url():
    return BASE_URL

@pytest.fixture(scope="module")
def send_request(base_url):
    def _send_request(method, endpoint, data=None, params=None):
        response = requests.request(method, endpoint, json=data, params=params)
        return response
    return _send_request

@pytest.fixture(scope="module")
def version_invalid_endpoint(base_url):
    return f"{base_url}/version1"

@pytest.fixture(scope="module")
def version_endpoint_url(base_url):
    return f"{base_url}/version"

@pytest.fixture(scope="module")
def json_endpoint_url(base_url):
    return f"{base_url}/json"

@pytest.fixture(scope="module")
def xml_endpoint_url(base_url):
    return f"{base_url}/xml"