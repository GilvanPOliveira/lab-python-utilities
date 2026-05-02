from pydantic import BaseModel, Field


class MarkdownTextRequest(BaseModel):
    content: str = Field(default="")


class MarkdownTableRequest(BaseModel):
    headers: list[str] = Field(min_length=1)
    rows: list[list[str]] = Field(default=[])


class MarkdownListRequest(BaseModel):
    items: list[str] = Field(min_length=1)
    ordered: bool = False


class MarkdownResultResponse(BaseModel):
    result: str
