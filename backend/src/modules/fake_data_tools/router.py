from fastapi import APIRouter

from src.modules.fake_data_tools.schemas import FakeDataRequest, FakeJsonRequest, LoremRequest
from src.modules.fake_data_tools.service import (
    generate_emails,
    generate_fake_json,
    generate_lorem,
    generate_names,
    generate_phones,
)

router = APIRouter()


@router.post("/lorem")
def lorem_route(payload: LoremRequest):
    return generate_lorem(payload.paragraphs)


@router.post("/names")
def names_route(payload: FakeDataRequest):
    return generate_names(payload.quantity)


@router.post("/emails")
def emails_route(payload: FakeDataRequest):
    return generate_emails(payload.quantity)


@router.post("/phones")
def phones_route(payload: FakeDataRequest):
    return generate_phones(payload.quantity)


@router.post("/json")
def fake_json_route(payload: FakeJsonRequest):
    return generate_fake_json(payload.quantity)
