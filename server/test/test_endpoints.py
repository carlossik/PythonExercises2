# test_endpoints.py
import pytest
import json
from jsonpath_ng import jsonpath, parse


class TestVersionEndpoint:
    # Test case 1: Valid GET Request
    def test_version_valid_get_request(self, version_endpoint_url, send_request):
        """REQ-1.1a"""
        response = send_request("GET", version_endpoint_url)
        assert response.status_code == 200

    # Test cases 2-7: Invalid HTTP Methods
    @pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    def test_version_invalid_http_methods(self, version_endpoint_url, send_request, method):
        """REQ-1.1b"""
        response = send_request(method, version_endpoint_url)
        assert response.status_code == 405

    def test_version_endpoint_ok_response_format(self, version_endpoint_url, send_request):
        """REQ-1.2"""
        response = send_request("GET", version_endpoint_url)
        assert response.status_code == 200
        try:
            json_response = response.json()
            jsonpath_expr = parse("$.success")
            success_result = jsonpath_expr.find(json_response)

            assert len(success_result) == 1
            assert success_result[0].value is True
            print(success_result[0])

            jsonpath_expr = parse("$.data.version")
            version_result = jsonpath_expr.find(json_response)

            assert len(version_result) == 1
            assert version_result[0].value

        except ValueError:
            pytest.fail("Failed to parse response body as JSON")

    @pytest.mark.parametrize("method", ["POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
    def test_version_invalid_http_method_format(self, version_endpoint_url, send_request, method):
        """REQ-1.3"""
        response = send_request(method, version_endpoint_url)
        assert response.status_code == 405

        assert response.json() == {"detail": "Method Not Allowed"}

    def test_invalid_url(self, version_invalid_endpoint, send_request):
        """REQ-1.3"""
        response = send_request("GET", version_invalid_endpoint)
        assert response.status_code == 404
        assert response.json() == {"detail": "Not Found"}


class TestJsonEndpoint:

    def test_json_valid_post_method(self, json_endpoint_url, send_request):
        """REQ-2.1a"""
        response = send_request("POST", json_endpoint_url)
        assert response.status_code == 400

    @pytest.mark.parametrize("method", ["GET", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
    def test_json_invalid_http_methods(self, json_endpoint_url, send_request, method):
        """REQ-2.1b"""
        response = send_request(method, json_endpoint_url)
        assert response.status_code == 405

    @pytest.mark.parametrize(
        "product_name, product_type, product_version",
        [
            ("SAVINGS", "type1", 1.1),
            ("LOANS", "type2", 2.1),
            ("MORTGAGES", "type3", 3.5),
            ("CREDITCARDS", "type4", 4.2),
            ("MORTGAGES", "", 3.5),
            ("CREDITCARDS", 3000, 43.2),
        ],
    )
    def test_json_valid_request_body_format_Ok(self, json_endpoint_url, send_request, product_name, product_type,
                                               product_version):
        """REQ-2.4"""
        data = {
            "product_name": product_name,
            "product_type": product_type,
            "product_version": product_version,
        }
        response = send_request("POST", json_endpoint_url, data)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "product_name, product_type, product_version",
        [
            pytest.param("", "type1", 1.1, id='Missing Product Name'),
            pytest.param("Saving", "type1", 1.1, id='Wrong Product Name'),
            pytest.param("LOANS", "", 1.1, id='Missing Product Type'),
            pytest.param("MORTGAGES", "type1", -1.1, id='Wrong Product Version'),
            pytest.param("CREDITCARDS", "type1", 1000, id='Wrong Product Version - Int'),
            pytest.param("MORTGAGES", "type1", -1.1, id='Missing Product Version'),
        ],
    )
    def test_json_invalid_data_request_body_format_Ok(self, json_endpoint_url, send_request, product_name, product_type,
                                                      product_version):
        """REQ-2.4"""
        data = {
            "product_name": product_name,
            "product_type": product_type,
            "product_version": product_version,
        }
        response = send_request("POST", json_endpoint_url, data)
        assert response.status_code == 400

    def test_returns_sub_200ms_response_time(self, json_endpoint_url, send_request):
        """REQ-2.5"""
        response = send_request("POST", json_endpoint_url)
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 0.2


class TestXmlEndpoint:
    def test_only_supports_get_method(self, xml_endpoint_url, send_request):
        """REQ-3.1"""
        for method in ["POST", "PUT"]:
            response = send_request(method, xml_endpoint_url)
            assert response.status_code == 405
            assert response.json() == {"detail": "Method Not Allowed"}

    @pytest.mark.parametrize("debug_value", [True, False])
    def test_with_debug_param(self, xml_endpoint_url, send_request, debug_value):
        """REQ-3.2, REQ-3.3, REQ-3.4, REQ-3.5"""
        params = {"debug": debug_value}
        response = send_request("GET", xml_endpoint_url, params=params)
        assert response.status_code == 201
        if debug_value:
            assert "<overall>Decline</overall>" not in response.text


def test_invalid_endpoint(send_request):
    """Additional"""
    response = send_request("GET", "invalid_endpoint")
    assert response.status_code == 404
