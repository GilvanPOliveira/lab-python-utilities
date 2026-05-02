from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.modules.color_tools.router import router as color_router
from src.modules.date_tools.router import router as date_router
from src.modules.document_tools.router import router as document_router
from src.modules.fake_data_tools.router import router as fake_data_router
from src.modules.file_tools.router import router as file_router
from src.modules.hash_tools.router import router as hash_router
from src.modules.image_tools.router import router as image_router
from src.modules.json_tools.router import router as json_router
from src.modules.link_tools.router import router as link_router
from src.modules.markdown_tools.router import router as markdown_router
from src.modules.media_tools.router import router as media_router
from src.modules.message_tools.router import router as message_router
from src.modules.password_tools.router import router as password_router
from src.modules.pdf_tools.router import router as pdf_router
from src.modules.qrcode_tools.router import router as qrcode_router
from src.modules.signature_tools.router import router as signature_router
from src.modules.slug_tools.router import router as slug_router
from src.modules.text_tools.router import router as text_router
from src.modules.unit_tools.router import router as unit_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }


app.include_router(qrcode_router, prefix="/api/qrcode", tags=["QR Code"])
app.include_router(password_router, prefix="/api/passwords", tags=["Passwords"])
app.include_router(json_router, prefix="/api/json", tags=["JSON"])
app.include_router(document_router, prefix="/api/documents", tags=["Documents"])
app.include_router(slug_router, prefix="/api/slug", tags=["Slug"])
app.include_router(text_router, prefix="/api/text", tags=["Text"])
app.include_router(hash_router, prefix="/api/hash", tags=["Hash"])
app.include_router(date_router, prefix="/api/dates", tags=["Dates"])
app.include_router(image_router, prefix="/api/images", tags=["Images"])
app.include_router(link_router, prefix="/api/links", tags=["Links"])
app.include_router(file_router, prefix="/api/files", tags=["Files"])
app.include_router(unit_router, prefix="/api/units", tags=["Units"])
app.include_router(color_router, prefix="/api/colors", tags=["Colors"])
app.include_router(markdown_router, prefix="/api/markdown", tags=["Markdown"])
app.include_router(fake_data_router, prefix="/api/fake-data", tags=["Fake Data"])
app.include_router(signature_router, prefix="/api/signatures", tags=["Signatures"])
app.include_router(message_router, prefix="/api/messages", tags=["Messages"])
app.include_router(pdf_router, prefix="/api/pdf", tags=["PDF"])
app.include_router(media_router, prefix="/api/media", tags=["Media"])
