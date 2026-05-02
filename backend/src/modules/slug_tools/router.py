from fastapi import APIRouter

from src.modules.slug_tools.schemas import SlugRequest, SlugResponse
from src.modules.slug_tools.service import generate_slug

router = APIRouter()


@router.post("/generate", response_model=SlugResponse)
def generate_slug_route(payload: SlugRequest):
    return generate_slug(payload)
