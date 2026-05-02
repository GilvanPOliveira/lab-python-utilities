from pydantic import BaseModel, Field


class PasswordRequest(BaseModel):
    length: int = Field(default=16, ge=6, le=128)
    include_uppercase: bool = True
    include_lowercase: bool = True
    include_numbers: bool = True
    include_symbols: bool = True


class PasswordResponse(BaseModel):
    password: str
    length: int
