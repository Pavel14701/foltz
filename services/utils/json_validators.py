from jsonschema import validate, ValidationError as JsonSchemaValidationError
from django.core.exceptions import ValidationError
import json


characteristics_schema = {
    "type": "object",
    "patternProperties": {
        "^.*$": {
            "type": ["string", "number", "array", "object", "boolean", "null"]
        }
    },
    "additionalProperties": True
}


def validate_characteristics(value):
    try:
        data = json.loads(value)
    except ValueError as e:
        raise ValidationError("Invalid JSON format") from e
    try:
        validate(instance=data, schema=characteristics_schema)
    except JsonSchemaValidationError as e:
        raise ValidationError(f"JSON schema validation error: {e.message}") from e


service_json_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "category": {"type": "string"},
        "subcategory": {"type": ["string", "null"]},
    },
    "required": ["title", "category"],
    "additionalProperties": False
}


def validate_service(value):
    try:
        data = json.loads(value)
    except ValueError as e:
        raise ValidationError("Invalid JSON format") from e
    try:
        validate(instance=data, schema=service_json_schema)
    except JsonSchemaValidationError as e:
        raise ValidationError(f"JSON schema validation error: {e.message}") from e