import decimal
import json
import os
import random

import boto3
from boto3.dynamodb.conditions import Key

dynamodb_table = boto3.resource("dynamodb").Table(os.getenv("TABLE"))


def lambda_handler(event, context):
    params = event.get("queryStringParameters", {})
    response = {"method": random_component_by_key("cooking")}

    if "no_sauce" not in params and response["method"]["use_sauce"]:
        response["sauce"] = random_component_by_key("sauce")

    if "no_dip" not in params:
        response["dip"] = random_component_by_key("dip")

    return json.dumps(response, cls=DecimalEncoder)


def random_component_by_key(component):
    results = dynamodb_table.query(
        KeyConditionExpression=Key("pk").eq(f"C#{component}"), ProjectionExpression="sk"
    )
    random_selection = random.choice(results["Items"])
    return dynamodb_table.get_item(
        Key={"pk": f"C#{component}", "sk": random_selection["sk"]},
        ProjectionExpression="#d",
        ExpressionAttributeNames={"#d": "data"},
    )["Item"]["data"]


def random_component_by_value(component):
    char = "".join(random.sample("abcdef1234567890", 3))

    def _result(sk):
        return dynamodb_table.query(
            KeyConditionExpression=Key("pk").eq(f"C#{component}") & sk,
            ProjectionExpression="#d",
            ExpressionAttributeNames={"#d": "data"},
            Limit=1,
        )["Items"][0]["data"]

    try:
        return _result(Key("sk").gt(f"ID#{char}"))
    except:
        return _result(Key("sk").lte(f"ID#{char}"))


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return json.JSONEncoder.default(self, obj)
