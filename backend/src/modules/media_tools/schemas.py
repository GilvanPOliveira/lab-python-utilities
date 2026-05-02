from pydantic import BaseModel, Field


class MediaUrlRequest(BaseModel):
    url: str = Field(min_length=1)


class MediaDownloadRequest(BaseModel):
    url: str = Field(min_length=1)
    output_format: str = "mp4"


class MediaInfoResponse(BaseModel):
    title: str
    uploader: str | None
    duration: int | None
    webpage_url: str
    thumbnail: str | None


class MediaFileResponse(BaseModel):
    filename: str
    mime_type: str
    content_base64: str
    size_bytes: int
