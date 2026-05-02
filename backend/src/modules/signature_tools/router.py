from fastapi import APIRouter

from src.modules.signature_tools.schemas import EmailSignatureRequest
from src.modules.signature_tools.service import generate_email_signature

router = APIRouter()


@router.post("/email")
def email_signature_route(payload: EmailSignatureRequest):
    return generate_email_signature(
        full_name=payload.full_name,
        role=payload.role,
        email=payload.email,
        phone=payload.phone,
        website=payload.website,
        github=payload.github,
        linkedin=payload.linkedin,
    )
