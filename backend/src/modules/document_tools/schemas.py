from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    value: str = Field(min_length=1)


class DocumentResponse(BaseModel):
    valid: bool
    value: str
    formatted: str | None = None
    digits: str
