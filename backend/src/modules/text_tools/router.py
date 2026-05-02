from fastapi import APIRouter

from src.modules.text_tools.schemas import (
    TextCleanResponse,
    TextConvertRequest,
    TextConvertResponse,
    TextCountResponse,
    TextRequest,
)
from src.modules.text_tools.service import clean_text, convert_text, count_text

router = APIRouter()


@router.post("/clean", response_model=TextCleanResponse)
def clean_text_route(payload: TextRequest):
    return clean_text(payload)


@router.post("/convert", response_model=TextConvertResponse)
def convert_text_route(payload: TextConvertRequest):
    return convert_text(payload)


@router.post("/count", response_model=TextCountResponse)
def count_text_route(payload: TextRequest):
    return count_text(payload)
