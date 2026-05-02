from pydantic import BaseModel, Field


class LoremRequest(BaseModel):
    paragraphs: int = Field(default=2, ge=1, le=10)


class FakeDataRequest(BaseModel):
    quantity: int = Field(default=5, ge=1, le=50)


class FakeJsonRequest(BaseModel):
    quantity: int = Field(default=3, ge=1, le=20)


class FakeDataResponse(BaseModel):
    result: str
