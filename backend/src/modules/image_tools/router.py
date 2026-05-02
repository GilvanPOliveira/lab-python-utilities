from fastapi import APIRouter, File, Form, UploadFile

from src.modules.image_tools.service import (
    compress_image,
    convert_image,
    remove_background,
    resize_image,
)

router = APIRouter()


@router.post("/resize")
async def resize_image_route(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...),
):
    return await resize_image(file=file, width=width, height=height)


@router.post("/convert")
async def convert_image_route(
    file: UploadFile = File(...),
    output_format: str = Form(...),
):
    return await convert_image(file=file, output_format=output_format)


@router.post("/compress")
async def compress_image_route(
    file: UploadFile = File(...),
    output_format: str = Form(default="webp"),
    quality: int = Form(default=75),
):
    return await compress_image(
        file=file,
        output_format=output_format,
        quality=quality,
    )


@router.post("/remove-background")
async def remove_background_route(file: UploadFile = File(...)):
    return await remove_background(file=file)
