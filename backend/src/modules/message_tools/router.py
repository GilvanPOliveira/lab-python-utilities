from fastapi import APIRouter

from src.modules.message_tools.schemas import QuickMessageRequest
from src.modules.message_tools.service import generate_quick_message

router = APIRouter()


@router.post("/quick")
def quick_message_route(payload: QuickMessageRequest):
    return generate_quick_message(
        message_type=payload.message_type,
        tone=payload.tone,
        recipient_name=payload.recipient_name,
        context=payload.context,
        objective=payload.objective,
    )
