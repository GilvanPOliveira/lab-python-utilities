import base64
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from fastapi import HTTPException
import yt_dlp

MAX_MEDIA_SIZE = 80 * 1024 * 1024
MAX_DURATION_SECONDS = 60 * 30


def validate_media_url(url: str) -> str:
    cleaned = url.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Informe uma URL válida.")

    if not cleaned.startswith(("http://", "https://")):
        cleaned = f"https://{cleaned}"

    parsed = urlparse(cleaned)

    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="URL inválida.")

    return cleaned


def validate_authorized_context() -> None:
    return None


def read_generated_file(path: Path, mime_type: str) -> dict:
    if not path.exists():
        raise HTTPException(status_code=500, detail="Arquivo gerado não encontrado.")

    content = path.read_bytes()

    if len(content) > MAX_MEDIA_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Arquivo gerado muito grande para retornar pela aplicação.",
        )

    return {
        "filename": path.name,
        "mime_type": mime_type,
        "content_base64": base64.b64encode(content).decode("utf-8"),
        "size_bytes": len(content),
    }


def get_media_info(url: str) -> dict:
    normalized = validate_media_url(url)

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(normalized, download=False)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível obter informações da mídia.",
        )

    duration = info.get("duration")

    return {
        "title": info.get("title") or "media",
        "uploader": info.get("uploader"),
        "duration": duration,
        "webpage_url": info.get("webpage_url") or normalized,
        "thumbnail": info.get("thumbnail"),
    }


def ensure_duration_allowed(info: dict) -> None:
    duration = info.get("duration")

    if duration and duration > MAX_DURATION_SECONDS:
        raise HTTPException(
            status_code=400,
            detail="Mídia muito longa. Limite atual: 30 minutos.",
        )


def find_first_file(directory: Path, extensions: set[str]) -> Path:
    files = [
        file
        for file in directory.iterdir()
        if file.is_file() and file.suffix.replace(".", "").lower() in extensions
    ]

    if not files:
        raise HTTPException(status_code=500, detail="Nenhum arquivo foi gerado.")

    files.sort(key=lambda file: file.stat().st_mtime, reverse=True)

    return files[0]


def download_video(url: str) -> dict:
    normalized = validate_media_url(url)
    info = get_media_info(normalized)
    ensure_duration_allowed(info)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "outtmpl": str(temp_path / "%(title).120s.%(ext)s"),
            "format": "best[ext=mp4]/best",
            "restrictfilenames": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([normalized])
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível baixar a mídia informada.",
            )

        output_file = find_first_file(temp_path, {"mp4", "webm", "mkv", "mov"})

        mime_type = "video/mp4" if output_file.suffix.lower() == ".mp4" else "application/octet-stream"

        return read_generated_file(output_file, mime_type)


def download_audio_mp3(url: str) -> dict:
    normalized = validate_media_url(url)
    info = get_media_info(normalized)
    ensure_duration_allowed(info)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
            "outtmpl": str(temp_path / "%(title).120s.%(ext)s"),
            "format": "bestaudio/best",
            "restrictfilenames": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([normalized])
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível converter a mídia para MP3. Verifique se o FFmpeg está instalado.",
            )

        output_file = find_first_file(temp_path, {"mp3"})

        return read_generated_file(output_file, "audio/mpeg")
