from pydantic import BaseModel, Field


class DateFormatRequest(BaseModel):
    value: str = Field(min_length=1)
    output_format: str = "%d/%m/%Y"


class DateDifferenceRequest(BaseModel):
    start_date: str = Field(min_length=1)
    end_date: str = Field(min_length=1)


class DateAddRequest(BaseModel):
    value: str = Field(min_length=1)
    days: int = 0
    months: int = 0
    years: int = 0
    operation: str = Field(default="add", pattern="^(add|subtract)$")
    output_format: str = "%d/%m/%Y"


class DateFormatResponse(BaseModel):
    original: str
    formatted: str
    iso: str
    timestamp: int
    detected_format: str


class DateDifferenceResponse(BaseModel):
    start_date: str
    end_date: str
    total_days: int
    absolute_days: int
    total_hours: int
    total_minutes: int
    total_seconds: int
    human_readable: str


class DateAddResponse(BaseModel):
    original: str
    result: str
    iso: str
    operation: str
    days: int
    months: int
    years: int
