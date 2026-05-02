from pydantic import BaseModel, Field


class HashRequest(BaseModel):
    value: str = Field(min_length=1)
    algorithm: str = Field(default="sha256", pattern="^(md5|sha1|sha256|sha512)$")


class HashResponse(BaseModel):
    algorithm: str
    hash: str
