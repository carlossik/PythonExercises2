import os
import sys
import dataclasses
from dataclasses import dataclass
from enum import auto
from typing import Optional
from collections import defaultdict
from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from strenum import UppercaseStrEnum
import random


sys.path.append(os.path.dirname(__file__))


from utilities import logged, Version


class ProductNames(UppercaseStrEnum):
    Savings = auto()
    Loans = auto()
    Mortgages = auto()
    CreditCard = auto()


@dataclass
class Product:
    product_name: ProductNames
    product_type: Optional[str] = None
    product_version: Optional[float] = None

    def __post_init__(self):
        if self.product_version < 0:
            self.product_version *= -1
        self.product_type = self.product_type.upper()


app = FastAPI()


@app.exception_handler(RequestValidationError)
def json_request_validation_exception_handler(request: Request, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Invalid request", "errors": reformatted_message}
        ),
    )


@app.get("/version/")
@app.delete("/version/")
def get_version():
    data = {
        "success": True,
        "data": {
            "version": Version
        }
    }
    return JSONResponse(content=data, media_type="application/json")


@app.post("/json/")
@logged
def create_json(product: Product):
    overall_result = "Accept"
    rule_decisions = []
    for index, rule_id in enumerate(range(0, random.randint(1, 12))):
        rule_outcome = random.choice(["Accept"] * 9 + ["Decline"])
        if rule_outcome == "Decline":
            overall_result = "Decline"
        rule_decisions.append({
            f"ruleA{index}": {
                "duration": random.random(),
                "result": rule_outcome
            }
        })
    data = {
        "format": "JSON",
        "data": dataclasses.asdict(product),
        "additional": {
            "overall": {
                "duration": 0.73890,
                "result": overall_result
            },
            "decisions": rule_decisions
        }
    }
    return JSONResponse(content=data, media_type="application/json")


@app.get("/xml/")
def read_xml(request: Request, debug: bool = False):
    debug_trace = ""
    if debug:
        req_headers = "".join([f"<{key} value='{value}'/>" for key, value in list(request.headers.items())])
        req_headers = f"<headers>{req_headers}</headers>"
        debug_trace = f"""
            <debug>
                <trace-id>2314-5641-sdf2-2344dfdf</trace-id>
                <request>
                    {req_headers}
                </request>
            </debug>
        """

    rule_xml = ""
    overall_result = "Accept"
    for rule_id in range(0, random.randint(1, 12)):
        rule_outcome = random.choice(["Accept"]*9 + ["Decline"])
        rule_xml += f"<rule id='{rule_id}'>{rule_outcome}</rule>"
    data = f"""
<xml version="1.0"?>
<data>
    {debug_trace if debug else ""}
    <decision_engine>
        <overall>{overall_result}</overall>
        <outcomes>
            {rule_xml}
        </outcomes>
    </decision_engine>
</data>
    """
    return Response(content=data, media_type="application/xml")
