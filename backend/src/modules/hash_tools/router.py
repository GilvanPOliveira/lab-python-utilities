from fastapi import APIRouter

from src.modules.hash_tools.schemas import HashRequest, HashResponse
from src.modules.hash_tools.service import generate_hash

router = APIRouter()


@router.post("/generate", response_model=HashResponse)
def generate_hash_route(payload: HashRequest):
    return generate_hash(payload)
