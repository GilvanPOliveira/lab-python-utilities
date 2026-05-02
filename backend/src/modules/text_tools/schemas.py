from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    value: str = Field(min_length=1)


class TextConvertRequest(TextRequest):
    mode: str = Field(pattern="^(upper|lower|title|capitalize)$")


class TextCleanResponse(BaseModel):
    original: str
    cleaned: str


class TextConvertResponse(BaseModel):
    original: str
    converted: str
    mode: str


class TextCountResponse(BaseModel):
    characters: int
    characters_without_spaces: int
    words: int
    lines: int
