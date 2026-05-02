from fastapi import APIRouter

from src.modules.password_tools.schemas import PasswordRequest, PasswordResponse
from src.modules.password_tools.service import generate_password

router = APIRouter()


@router.post("/generate", response_model=PasswordResponse)
def create_password(payload: PasswordRequest):
    return generate_password(payload)
