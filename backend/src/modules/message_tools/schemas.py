from pydantic import BaseModel, Field


class QuickMessageRequest(BaseModel):
    message_type: str = Field(min_length=1)
    tone: str = "profissional"
    recipient_name: str = ""
    context: str = ""
    objective: str = ""


class QuickMessageResponse(BaseModel):
    title: str
    message: str
