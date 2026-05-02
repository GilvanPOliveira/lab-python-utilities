from fastapi import APIRouter

from src.modules.qrcode_tools.schemas import QrCodeRequest, QrCodeResponse
from src.modules.qrcode_tools.service import generate_qrcode

router = APIRouter()


@router.post("/generate", response_model=QrCodeResponse)
def create_qrcode(payload: QrCodeRequest):
    return generate_qrcode(payload)
