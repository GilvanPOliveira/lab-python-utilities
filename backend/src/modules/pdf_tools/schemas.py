from pydantic import BaseModel, Field


class SplitPdfRequest(BaseModel):
    start_page: int = Field(ge=1)
    end_page: int = Field(ge=1)


class PdfFileResponse(BaseModel):
    filename: str
    mime_type: str
    content_base64: str
    size_bytes: int


class PdfTextResponse(BaseModel):
    filename: str
    pages: int
    text: str
