import base64
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader, PdfWriter

MAX_PDF_SIZE = 15 * 1024 * 1024


async def read_pdf_upload(file: UploadFile) -> tuple[bytes, PdfReader]:
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Arquivo PDF vazio.")

    if len(content) > MAX_PDF_SIZE:
        raise HTTPException(
            status_code=400,
            detail="PDF muito grande. Envie um arquivo de até 15 MB.",
        )

    if file.content_type and file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=400, detail="Envie um arquivo PDF válido.")

    try:
        reader = PdfReader(BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Não foi possível ler o PDF.")

    if len(reader.pages) == 0:
        raise HTTPException(status_code=400, detail="O PDF não possui páginas.")

    return content, reader


def encode_pdf(writer: PdfWriter, filename: str) -> dict:
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)

    content = buffer.getvalue()

    return {
        "filename": filename,
        "mime_type": "application/pdf",
        "content_base64": base64.b64encode(content).decode("utf-8"),
        "size_bytes": len(content),
    }


def safe_pdf_name(filename: str | None, suffix: str) -> str:
    stem = Path(filename or "documento").stem or "documento"
    safe = "".join(char for char in stem if char.isalnum() or char in ("-", "_")).strip()

    return f"{safe or 'documento'}-{suffix}.pdf"


async def merge_pdfs(files: list[UploadFile]) -> dict:
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Envie pelo menos dois PDFs para juntar.")

    writer = PdfWriter()

    for file in files:
        _, reader = await read_pdf_upload(file)

        for page in reader.pages:
            writer.add_page(page)

    return encode_pdf(writer, "pdf-merged.pdf")


async def split_pdf(file: UploadFile, start_page: int, end_page: int) -> dict:
    _, reader = await read_pdf_upload(file)
    total_pages = len(reader.pages)

    if start_page > end_page:
        raise HTTPException(status_code=400, detail="A página inicial não pode ser maior que a final.")

    if end_page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"O PDF possui apenas {total_pages} página(s).",
        )

    writer = PdfWriter()

    for page_index in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_index])

    return encode_pdf(writer, safe_pdf_name(file.filename, f"pages-{start_page}-{end_page}"))


async def extract_pdf_text(file: UploadFile) -> dict:
    _, reader = await read_pdf_upload(file)

    texts = []

    for index, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        texts.append(f"--- Página {index + 1} ---\n{text.strip()}")

    return {
        "filename": file.filename or "documento.pdf",
        "pages": len(reader.pages),
        "text": "\n\n".join(texts).strip(),
    }
