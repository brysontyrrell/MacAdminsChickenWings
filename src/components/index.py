import json
import os
import uuid

import boto3
import jsonschema

dynamodb_table = boto3.resource("dynamodb").Table(os.getenv("TABLE"))

COOKING_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "method", "temperature", "time"],
    "properties": {
        "type": {"type": "string", "enum": ["traditional", "boneless"]},
        "method": {"type": "string"},
        "temperature": {"type": "number"},
        "time": {"type": "number"},
        "ingredients": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "instructions": {"type": "array", "items": {"type": "string", "minItems": 1}},
    },
    "allOf": [
        {
            "if": {"properties": {"type": {"const": "traditional"}}},
            "then": {"properties": {"type": {"enum": ["baked", "fried", "smoked"]}}},
        },
        {
            "if": {"properties": {"type": {"const": "boneless"}}},
            "then": {"properties": {"type": {"enum": ["baked", "fried"]}}},
        },
    ],
}

SAUCE_DIP_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["name", "ingredients", "instructions"],
    "properties": {
        "name": {"type": "string"},
        "ingredients": {"type": "array", "items": {"type": "string", "minItems": 1}},
        "instructions": {"type": "array", "items": {"type": "string", "minItems": 1}},
    },
}


def lambda_handler(event, context):
    if event["rawPath"] == "/components/cooking-methods":
        schema = COOKING_SCHEMA
        pk = "C#cooking"

    elif event["rawPath"] == "/components/sauces":
        schema = SAUCE_DIP_SCHEMA
        pk = "C#sauce"

    elif event["rawPath"] == "/components/dips":
        schema = SAUCE_DIP_SCHEMA
        pk = "C#dip"

    else:
        raise Exception("Invalid Path")

    try:
        request_body = json.loads(event.get("body", "{}"))
        jsonschema.validate(request_body, schema=schema)
    except Exception as error:
        print(error)
        return {"statusCode": 400, "body": "Bad Request"}

    item_id = str(uuid.uuid4())
    item_data = {"id": item_id, **request_body}

    dynamodb_table.put_item(Item={"pk": pk, "sk": f"ID#{item_id}", "data": item_data})

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item_data),
    }
