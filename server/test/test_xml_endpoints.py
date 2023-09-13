import pytest
import json
from jsonpath_ng import jsonpath, parse
from xml.etree.ElementTree import fromstring

import pytest
import requests
from xml.etree import ElementTree as ET
from server.test.conftest import determine_overall_decision


from server.test.conftest import get_xml, xml_endpoint_url, send_request


class TestXmlEndpoint:

    @pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH", "OPTIONS", "POST", "HEAD"])
    def test_only_supports_get_method(self, xml_endpoint_url, send_request, method):
        """REQ-3.1"""
        response = send_request(method, xml_endpoint_url)
        if method == "GET":
            assert response.status_code == 200
        else:
            assert response.status_code == 405
            print(response.text)
            assert response.text == '{"detail":"Method Not Allowed"}'

    @pytest.mark.parametrize("debug_value", [True, False])
    def test_with_debug_param(self, xml_endpoint_url, send_request, debug_value):
        """REQ-3.2, REQ-3.3, REQ-3.4, REQ-3.5"""
        params = {"debug": debug_value}
        response = send_request("GET", xml_endpoint_url, params=params)
        assert response.status_code == 201
        if debug_value:
            assert "<overall>Decline</overall>" not in response.text

    def test_success_response_code(self, xml_endpoint_url, send_request):
        response = send_request("GET", xml_endpoint_url)
        assert response.status_code == 200, "Expected status code 201 but got another!"

    def test_response_format(self, xml_endpoint_url, send_request, parse_xml):
        response = send_request("GET", xml_endpoint_url)
        root = response.content
        assert root.tag == 'xml', "Root tag is not 'xml'!"

        data = root.find('data')
        assert data is not None, "'data' tag not found!"

        debug = data.find('debug')
        assert debug is not None, "'debug' tag not found!"

        decision_engine = data.find('decision_engine')
        assert decision_engine is not None, "'decision_engine' tag not found!"

    def test_decision_logic(self, fetch_and_parse_xml):

        response = fetch_and_parse_xml
        decision_engine = response.find('data').find('decision_engine')
        overall = decision_engine.find('overall').text

        outcomes = decision_engine.find('outcomes')
        rules = outcomes.findall('rule')

        if any(rule.text == 'Decline' for rule in rules):
            assert overall == 'Decline', "'overall' value is not 'Decline' even though one of the rules is 'Decline'"
        else:
            assert overall == 'Accept', "'overall' value is not 'Accept' even though none of the rules is 'Decline'"

    def test_query_param(self, xml_endpoint_url, debug_value_random, send_request):
        params = {"debug": debug_value_random}
        response = send_request("GET", xml_endpoint_url, params=params)
        assert response.status_code == 400, "Invalid query parameter value is accepted!"

    """[REQ-3.3] A successful call to the POST /xml endpoint returns a status code of 201"""
    """This is wrong because the requirement states that the only method for the xml endpoint is GET so these tests will fail"""

    def test_post_call_to_xml_endpoint(self, xml_endpoint_url,
                                       send_request):  # This test is always going to fail as the xml endpoint only supports a GET method
        response = send_request("POST", xml_endpoint_url)
        assert response.status_code == 200

    def test_body_of_response_of_post_call(self, xml_endpoint_url, send_request,
                                           get_xml_response_data):  # This test will always fail as the end point doesnt support post calls
        response = send_request("POST", xml_endpoint_url)
        assert response.text == get_xml_response_data




    def test_overall_decline_due_to_one_rule(self):
        xml_sample = '''
        <data>
            <decision_engine>
                <overall>Accept</overall>
                <outcomes>
                    <rule id='0'>Accept</rule>
                    <rule id='1'>Decline</rule>
                    <rule id='2'>Accept</rule>
                </outcomes>
            </decision_engine>
        </data>
        '''
        assert determine_overall_decision(xml_sample) == 'Decline'

    def test_overall_decline_due_to_all_rules(self):
        xml_sample = '''
        <data>
            <decision_engine>
                <overall>Accept</overall>
                <outcomes>
                    <rule id='0'>Decline</rule>
                    <rule id='1'>Decline</rule>
                    <rule id='2'>Decline</rule>
                </outcomes>
            </decision_engine>
        </data>
        '''
        assert determine_overall_decision(xml_sample) == 'Decline'

    def test_overall_accept(self):
        xml_sample = '''
        <data>
            <decision_engine>
                <overall>Accept</overall>
                <outcomes>
                    <rule id='0'>Accept</rule>
                    <rule id='1'>Accept</rule>
                    <rule id='2'>Accept</rule>
                </outcomes>
            </decision_engine>
        </data>
        '''
        assert determine_overall_decision(xml_sample) == 'Accept'

