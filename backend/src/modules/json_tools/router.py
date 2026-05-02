from fastapi import APIRouter

from src.modules.json_tools.schemas import JsonResponse, JsonTextRequest
from src.modules.json_tools.service import format_json, minify_json, validate_json

router = APIRouter()


@router.post("/format", response_model=JsonResponse)
def format_json_route(payload: JsonTextRequest):
    return format_json(payload)


@router.post("/validate", response_model=JsonResponse)
def validate_json_route(payload: JsonTextRequest):
    return validate_json(payload)


@router.post("/minify", response_model=JsonResponse)
def minify_json_route(payload: JsonTextRequest):
    return minify_json(payload)
