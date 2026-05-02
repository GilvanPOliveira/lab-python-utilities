from fastapi import APIRouter

from src.modules.link_tools.schemas import ShortenUrlRequest, UrlInputRequest, UrlTextRequest
from src.modules.link_tools.service import (
    clean_url,
    decode_url_value,
    encode_url_value,
    shorten_url,
)

router = APIRouter()


@router.post("/shorten")
async def shorten_url_route(payload: ShortenUrlRequest):
    return await shorten_url(
        url=payload.url,
        custom_code=payload.custom_code,
    )


@router.post("/clean")
def clean_url_route(payload: UrlInputRequest):
    return clean_url(payload.url)


@router.post("/encode")
def encode_url_route(payload: UrlTextRequest):
    return encode_url_value(payload.value)


@router.post("/decode")
def decode_url_route(payload: UrlTextRequest):
    return decode_url_value(payload.value)
