# Requirements

## Version Endpoint

### Request

[REQ-1.1] The /version endpoint only supports the GET method.

### Response

[REQ-1.2] The /version endpoint returns a status code of '200 OK' and a response body of the format:

```json
  {
    "success": true,
    "data": {
        "version": "<Version>"
    }
  }
```

[REQ-1.3] Any other HTTP methods executed against the /version endpoint will return a status code of '405 Method Not Allowed' and a response body of the format:

```json
{
    "detail": "Method Not Allowed"
}
```

## JSON Endpoint

### Request

[REQ-2.1] The /json endpoint only supports the POST method.

[REQ-2.2] The request body for the /json endpoint is of the format:

```json
{
    "product_name": "<String>",
    "product_type": "<String>",
    "product_version": "<Float>"
}
```

Where the data must obey the following conditions:

| Field Name | Data Type | Allowed Values                         |
|------------|-----------|----------------------------------------|
| product_name | String | SAVINGS, LOANS, MORTGAGES, CREDITCARDS |
| product_type | String | Any                                    |
| product_version | Float | Positive floats (E.g. 1.1, 2.1)        |

### Response

[REQ-2.3] The successful response body of the /json endpoint is of the format

```json
{
    "format": "JSON",
    "data": {
        "product_name": "<String>",
        "product_type": "<String>",
        "product_version": ",<Float>"
    },
    "additional": {
        "overall": {
            "duration": "<Float>",
            "result": "<String>"
        },
        "decisions": [
            {
                "rule[Code]": {
                    "duration":" <Float>",
                    "result": "<String>"
                }
              
            }
        ]
    }
}
```

The 'rule[Code]' section would be duplicated in the response per rule execution.

[REQ-2.4] All other methods will result in a status code of '405 Method Not Allowed' and a response body of the format:

```json
{
    "detail": "Method Not Allowed"
}
```

[REQ-2.5] The/response time for the /json call should always be a sub 200ms response time.

## XML Endpoint

### Request

[REQ-3.1] The /xml endpoint only supports the GET method.

[REQ-3.2] The /xml endpoint supports a single query parameter:

| Query Parameter | Allowed Values |
|-----------------|----------------|
| debug           | True, False    |

### Response

[REQ-3.3] A successful call to the POST /xml endpoint returns a status code of 201

[REQ-3.4] The body of a successful call to the POST /xml endpoint will be of the format:

```xml

<xml version="1.0"?>
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
```

[REQ-3.5] The 'data/decision_engine/overall' item should be 'Accept' unless one of the rules has an outcome of 'Decline' in which case the overall result should be 'Decline'
