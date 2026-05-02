from fastapi import APIRouter, File, UploadFile

from src.modules.file_tools.service import extract_metadata

router = APIRouter()


@router.post("/metadata")
async def metadata_route(file: UploadFile = File(...)):
    return await extract_metadata(file)
