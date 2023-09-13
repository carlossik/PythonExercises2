There are a few things to note in regard to this assignment


1. Tests have been split into two different files aas they were getting too big . we now have test_xml_endpoints and test_endpoints.
2. [REQ-3.1]  states explicitly that The /xml endpoint only supports the GET method but in [REQ-3.3]  we are asked to verify that "A successful call to the POST /xml endpoint returns a status code of 201" which will always fail
and also asked to verify [REQ-3.4] The body of a successful call to the POST /xml endpoint will be of a certain format which will always fail becauase the endpoint only supports a GET method
