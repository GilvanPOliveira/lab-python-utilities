from pydantic import BaseModel, Field


class SlugRequest(BaseModel):
    value: str = Field(min_length=1)


class SlugResponse(BaseModel):
    original: str
    slug: str
