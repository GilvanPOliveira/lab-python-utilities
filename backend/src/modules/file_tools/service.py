from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

MAX_FILE_SIZE = 10 * 1024 * 1024


async def extract_metadata(file: UploadFile) -> dict:
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Arquivo muito grande. Limite máximo: 10 MB.",
        )

    filename = file.filename or "arquivo"
    extension = Path(filename).suffix.replace(".", "").lower()

    metadata = {
        "filename": filename,
        "extension": extension,
        "mime_type": file.content_type,
        "size_bytes": len(content),
        "size_kb": round(len(content) / 1024, 2),
        "size_mb": round(len(content) / 1024 / 1024, 2),
        "is_image": False,
        "image_format": None,
        "width": None,
        "height": None,
        "color_mode": None,
    }

    try:
        image = Image.open(BytesIO(content))
        image.load()

        metadata.update(
            {
                "is_image": True,
                "image_format": image.format,
                "width": image.width,
                "height": image.height,
                "color_mode": image.mode,
            }
        )
    except (UnidentifiedImageError, OSError):
        pass

    return metadata
