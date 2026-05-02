import base64
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_DIMENSION = 4000
ALLOWED_FORMATS = {"png", "jpg", "jpeg", "webp"}

Image.MAX_IMAGE_PIXELS = 25_000_000


def normalize_output_format(output_format: str) -> tuple[str, str, str]:
    normalized = output_format.lower().strip()

    if normalized not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail="Formato inválido. Use png, jpg, jpeg ou webp.",
        )

    if normalized in {"jpg", "jpeg"}:
        return "JPEG", "jpg", "image/jpeg"

    if normalized == "webp":
        return "WEBP", "webp", "image/webp"

    return "PNG", "png", "image/png"


def validate_dimensions(width: int, height: int) -> None:
    if width < 1 or height < 1:
        raise HTTPException(
            status_code=400,
            detail="Largura e altura devem ser maiores que zero.",
        )

    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise HTTPException(
            status_code=400,
            detail=f"Largura e altura não podem passar de {MAX_DIMENSION}px.",
        )


async def read_image_file(file: UploadFile) -> tuple[bytes, Image.Image]:
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Arquivo muito grande. Envie uma imagem de até 5 MB.",
        )

    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Arquivo inválido. Envie uma imagem.",
        )

    try:
        image = Image.open(BytesIO(content))
        image.load()
        return content, image
    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Não foi possível ler a imagem enviada.",
        )


def prepare_image_for_output(image: Image.Image, pil_format: str) -> Image.Image:
    if pil_format == "JPEG" and image.mode in {"RGBA", "P", "LA"}:
        background = Image.new("RGB", image.size, (255, 255, 255))

        if image.mode == "P":
            image = image.convert("RGBA")

        mask = image.split()[-1] if image.mode in {"RGBA", "LA"} else None
        background.paste(image, mask=mask)

        return background

    if pil_format in {"PNG", "WEBP"} and image.mode not in {"RGB", "RGBA"}:
        return image.convert("RGBA")

    return image


def image_to_base64(image: Image.Image, pil_format: str, quality: int = 90) -> tuple[str, int]:
    buffer = BytesIO()
    save_kwargs = {}

    if pil_format in {"JPEG", "WEBP"}:
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True

    if pil_format == "PNG":
        save_kwargs["optimize"] = True

    image.save(buffer, format=pil_format, **save_kwargs)
    buffer.seek(0)

    content = buffer.getvalue()
    image_base64 = base64.b64encode(content).decode("utf-8")

    return image_base64, len(content)


def image_bytes_to_base64(content: bytes) -> str:
    return base64.b64encode(content).decode("utf-8")


def build_filename(original_filename: str | None, suffix: str, extension: str) -> str:
    if not original_filename:
        return f"image-{suffix}.{extension}"

    stem = Path(original_filename).stem or "image"
    return f"{stem}-{suffix}.{extension}"


async def resize_image(file: UploadFile, width: int, height: int) -> dict:
    validate_dimensions(width, height)

    original_content, image = await read_image_file(file)
    original_width, original_height = image.size
    original_format = image.format or "UNKNOWN"

    resized = image.resize((width, height), Image.Resampling.LANCZOS)
    output = prepare_image_for_output(resized, "PNG")
    image_base64, output_size = image_to_base64(output, "PNG")

    return {
        "image_base64": image_base64,
        "mime_type": "image/png",
        "filename": build_filename(file.filename, "resized", "png"),
        "original_format": original_format,
        "original_width": original_width,
        "original_height": original_height,
        "original_size_bytes": len(original_content),
        "output_format": "PNG",
        "output_width": width,
        "output_height": height,
        "output_size_bytes": output_size,
    }


async def convert_image(file: UploadFile, output_format: str) -> dict:
    pil_format, extension, mime_type = normalize_output_format(output_format)

    original_content, image = await read_image_file(file)
    original_width, original_height = image.size
    original_format = image.format or "UNKNOWN"

    output = prepare_image_for_output(image, pil_format)
    image_base64, output_size = image_to_base64(output, pil_format)

    return {
        "image_base64": image_base64,
        "mime_type": mime_type,
        "filename": build_filename(file.filename, "converted", extension),
        "original_format": original_format,
        "original_width": original_width,
        "original_height": original_height,
        "original_size_bytes": len(original_content),
        "output_format": pil_format,
        "output_width": original_width,
        "output_height": original_height,
        "output_size_bytes": output_size,
    }


async def compress_image(file: UploadFile, output_format: str, quality: int) -> dict:
    if quality < 1 or quality > 100:
        raise HTTPException(status_code=400, detail="A qualidade deve estar entre 1 e 100.")

    pil_format, extension, mime_type = normalize_output_format(output_format)

    original_content, image = await read_image_file(file)
    original_width, original_height = image.size
    original_format = image.format or "UNKNOWN"

    output = prepare_image_for_output(image, pil_format)
    image_base64, output_size = image_to_base64(output, pil_format, quality)

    return {
        "image_base64": image_base64,
        "mime_type": mime_type,
        "filename": build_filename(file.filename, "compressed", extension),
        "original_format": original_format,
        "original_width": original_width,
        "original_height": original_height,
        "original_size_bytes": len(original_content),
        "output_format": pil_format,
        "output_width": original_width,
        "output_height": original_height,
        "output_size_bytes": output_size,
    }


async def remove_background(file: UploadFile) -> dict:
    original_content, image = await read_image_file(file)
    original_width, original_height = image.size
    original_format = image.format or "UNKNOWN"

    try:
        from rembg import remove
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="A dependência rembg não está instalada no backend.",
        )

    try:
        output_content = remove(original_content, force_return_bytes=True)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível remover o fundo da imagem.",
        )

    return {
        "image_base64": image_bytes_to_base64(output_content),
        "mime_type": "image/png",
        "filename": build_filename(file.filename, "no-background", "png"),
        "original_format": original_format,
        "original_width": original_width,
        "original_height": original_height,
        "original_size_bytes": len(original_content),
        "output_format": "PNG",
        "output_width": original_width,
        "output_height": original_height,
        "output_size_bytes": len(output_content),
    }
