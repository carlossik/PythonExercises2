from xml.etree.ElementTree import fromstring

import pytest
import requests
from xml.etree import ElementTree as ET
BASE_URL = "http://127.0.0.1:8000"
BASE_URL2 = "http://127.0.0.1:8002"




xml_response_data = """<xml version="1.0">
<data>
    <debug>
        <trace-id>2314-5641-sdf2-2344dfdf</trace-id>
        <request>
            <headers>
                <content-type value='application/json'/>
                <user-agent value='PostmanRuntime/7.29.0'/>
                <accept value='*/*'/>
                <postman-token value='774a3c2b-c7f1-4c45-b2ff-e53400c4dc0d'/>
                <accept-encoding value='gzip, deflate, br'/>
                <connection value='keep-alive'/>
                <content-length value='91'/>
                <referer value='http://localhost:8000/xml?debug=True'/>
                <host value='localhost:8000'/>
            </headers>
        </request>
    </debug>
    <decision_engine>
        <overall>Accept</overall>
        <outcomes>
            <rule id='0'>Accept</rule>
            <rule id='1'>Accept</rule>
            <rule id='2'>Accept</rule>
        </outcomes>
    </decision_engine>
</data>
```"""




@pytest.fixture(scope="module")
def fake_base_url():
    return BASE_URL2


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


@pytest.fixture(scope="module")
def get_xml(debug_value):
    response = requests.get(f"{base_url}/xml", params={'debug': debug_value})
    return response

@pytest.fixture(scope="module")
def fetch_and_parse_xml(base_url):
    response = requests.get(f"{base_url}/xml")
    response.raise_for_status()
    root = ET.parse(fromstring(response.content))
    return root

@pytest.fixture(scope="module")
def debug_value_random():
    return "randon_value"

@pytest.fixture(scope="module")
def get_xml_respomse_data():
    return xml_response_data


def determine_overall_decision(xmlcontent):
    # Parse the XML content
    root = ET.fromstring(xmlcontent)
    # Check individual rules
    for rule in root.findall('./decision_engine/outcomes/rule'):
        if rule.text == 'Decline':
            return 'Decline'
    return 'Accept'