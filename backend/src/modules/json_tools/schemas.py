from typing import Any

from pydantic import BaseModel


class JsonTextRequest(BaseModel):
    content: str


class JsonResponse(BaseModel):
    valid: bool
    result: str | None = None
    error: str | None = None
    data: Any | None = None
