from pydantic import BaseModel


class FileMetadataResponse(BaseModel):
    filename: str
    extension: str
    mime_type: str | None
    size_bytes: int
    size_kb: float
    size_mb: float
    is_image: bool
    image_format: str | None = None
    width: int | None = None
    height: int | None = None
    color_mode: str | None = None
