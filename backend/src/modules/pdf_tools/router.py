from fastapi import APIRouter, File, Form, UploadFile

from src.modules.pdf_tools.service import extract_pdf_text, merge_pdfs, split_pdf

router = APIRouter()


@router.post("/merge")
async def merge_pdf_route(files: list[UploadFile] = File(...)):
    return await merge_pdfs(files)


@router.post("/split")
async def split_pdf_route(
    file: UploadFile = File(...),
    start_page: int = Form(...),
    end_page: int = Form(...),
):
    return await split_pdf(file, start_page, end_page)


@router.post("/extract-text")
async def extract_text_route(file: UploadFile = File(...)):
    return await extract_pdf_text(file)
