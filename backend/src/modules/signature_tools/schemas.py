from pydantic import BaseModel


class EmailSignatureRequest(BaseModel):
    full_name: str
    role: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""
    github: str = ""
    linkedin: str = ""


class EmailSignatureResponse(BaseModel):
    html: str
    plain_text: str
