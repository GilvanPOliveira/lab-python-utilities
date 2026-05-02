from pydantic import BaseModel, Field


class UrlInputRequest(BaseModel):
    url: str = Field(min_length=1)


class UrlTextRequest(BaseModel):
    value: str = Field(min_length=1)


class ShortenUrlRequest(BaseModel):
    url: str = Field(min_length=1)
    custom_code: str | None = Field(default=None, min_length=5, max_length=30)


class CleanUrlResponse(BaseModel):
    original_url: str
    cleaned_url: str
    removed_params: list[str]
    domain: str | None
    is_valid: bool


class UrlEncodeResponse(BaseModel):
    original: str
    encoded: str


class UrlDecodeResponse(BaseModel):
    original: str
    decoded: str


class ShortenUrlResponse(BaseModel):
    original_url: str
    short_url: str
    provider: str
