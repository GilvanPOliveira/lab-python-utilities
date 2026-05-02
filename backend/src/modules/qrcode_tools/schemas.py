from pydantic import BaseModel, Field


class QrCodeRequest(BaseModel):
    data: str = Field(min_length=1)
    box_size: int = Field(default=10, ge=1, le=40)
    border: int = Field(default=4, ge=0, le=20)


class QrCodeResponse(BaseModel):
    image_base64: str
    mime_type: str
    filename: str
