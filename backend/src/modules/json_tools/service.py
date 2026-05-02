import json

from src.modules.json_tools.schemas import JsonTextRequest


def format_json(payload: JsonTextRequest) -> dict:
    try:
        parsed = json.loads(payload.content)
        return {
            "valid": True,
            "result": json.dumps(parsed, indent=2, ensure_ascii=False),
            "error": None,
            "data": parsed,
        }
    except json.JSONDecodeError as error:
        return {
            "valid": False,
            "result": None,
            "error": str(error),
            "data": None,
        }


def validate_json(payload: JsonTextRequest) -> dict:
    try:
        parsed = json.loads(payload.content)
        return {
            "valid": True,
            "result": None,
            "error": None,
            "data": parsed,
        }
    except json.JSONDecodeError as error:
        return {
            "valid": False,
            "result": None,
            "error": str(error),
            "data": None,
        }


def minify_json(payload: JsonTextRequest) -> dict:
    try:
        parsed = json.loads(payload.content)
        return {
            "valid": True,
            "result": json.dumps(parsed, separators=(",", ":"), ensure_ascii=False),
            "error": None,
            "data": parsed,
        }
    except json.JSONDecodeError as error:
        return {
            "valid": False,
            "result": None,
            "error": str(error),
            "data": None,
        }
