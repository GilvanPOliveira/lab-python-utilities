from fastapi import APIRouter

from src.modules.date_tools.schemas import (
    DateAddRequest,
    DateAddResponse,
    DateDifferenceRequest,
    DateDifferenceResponse,
    DateFormatRequest,
    DateFormatResponse,
)
from src.modules.date_tools.service import (
    add_to_date,
    difference_between_dates,
    format_date,
)

router = APIRouter()


@router.post("/format", response_model=DateFormatResponse)
def format_date_route(payload: DateFormatRequest):
    return format_date(payload)


@router.post("/difference", response_model=DateDifferenceResponse)
def difference_between_dates_route(payload: DateDifferenceRequest):
    return difference_between_dates(payload)


@router.post("/add", response_model=DateAddResponse)
def add_to_date_route(payload: DateAddRequest):
    return add_to_date(payload)
