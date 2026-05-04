import base64
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from fastapi import HTTPException
import yt_dlp

MAX_MEDIA_SIZE = 80 * 1024 * 1024
MAX_DURATION_SECONDS = 60 * 30


@dataclass
class GeneratedMediaFile:
    path: Path
    mime_type: str
    cleanup_dir: Path


def validate_media_url(url: str) -> str:
    cleaned = url.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Informe uma URL valida.")

    if not cleaned.startswith(("http://", "https://")):
        cleaned = f"https://{cleaned}"

    parsed = urlparse(cleaned)

    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="URL invalida.")

    return cleaned


def validate_authorized_context() -> None:
    return None


def cleanup_generated_media(directory: Path) -> None:
    shutil.rmtree(directory, ignore_errors=True)


def resolve_ffmpeg_location() -> str | None:
    ffmpeg_path = shutil.which("ffmpeg")

    if ffmpeg_path:
        return ffmpeg_path

    try:
        import imageio_ffmpeg
    except ImportError:
        return None

    return imageio_ffmpeg.get_ffmpeg_exe()


def read_generated_file(path: Path, mime_type: str) -> dict:
    if not path.exists():
        raise HTTPException(status_code=500, detail="Arquivo gerado nao encontrado.")

    content = path.read_bytes()

    if len(content) > MAX_MEDIA_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Arquivo gerado muito grande para retornar pela aplicacao.",
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
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Nao foi possivel obter informacoes da midia: {exc}",
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
            detail="Midia muito longa. Limite atual: 30 minutos.",
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


def ensure_file_size_allowed(path: Path) -> None:
    if path.stat().st_size > MAX_MEDIA_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Arquivo gerado muito grande para retornar pela aplicacao.",
        )


def download_video(url: str) -> GeneratedMediaFile:
    normalized = validate_media_url(url)
    info = get_media_info(normalized)
    ensure_duration_allowed(info)

    temp_path = Path(tempfile.mkdtemp(prefix="media-video-"))
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "noplaylist": True,
        "outtmpl": str(temp_path / "%(title).120s.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "restrictfilenames": True,
        "merge_output_format": "mp4",
    }

    ffmpeg_location = resolve_ffmpeg_location()
    if ffmpeg_location:
        ydl_opts["ffmpeg_location"] = ffmpeg_location

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([normalized])
        output_file = find_first_file(temp_path, {"mp4", "webm", "mkv", "mov"})
        ensure_file_size_allowed(output_file)
    except HTTPException:
        cleanup_generated_media(temp_path)
        raise
    except Exception as exc:
        cleanup_generated_media(temp_path)
        raise HTTPException(
            status_code=400,
            detail=f"Nao foi possivel baixar a midia informada: {exc}",
        )

    mime_type = "video/mp4" if output_file.suffix.lower() == ".mp4" else "application/octet-stream"

    return GeneratedMediaFile(output_file, mime_type, temp_path)


def download_audio_mp3(url: str) -> GeneratedMediaFile:
    normalized = validate_media_url(url)
    info = get_media_info(normalized)
    ensure_duration_allowed(info)

    ffmpeg_location = resolve_ffmpeg_location()

    if not ffmpeg_location:
        raise HTTPException(
            status_code=500,
            detail="FFmpeg nao encontrado. Instale FFmpeg ou a dependencia imageio-ffmpeg.",
        )

    temp_path = Path(tempfile.mkdtemp(prefix="media-audio-"))
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "noplaylist": True,
        "outtmpl": str(temp_path / "%(title).120s.%(ext)s"),
        "format": "bestaudio/best",
        "restrictfilenames": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([normalized])
        source_file = find_first_file(
            temp_path,
            {"aac", "flac", "m4a", "mkv", "mov", "mp3", "mp4", "ogg", "opus", "wav", "webm"},
        )

        if source_file.suffix.lower() == ".mp3":
            output_file = source_file
        else:
            output_file = source_file.with_suffix(".mp3")
            subprocess.run(
                [
                    ffmpeg_location,
                    "-y",
                    "-i",
                    str(source_file),
                    "-vn",
                    "-codec:a",
                    "libmp3lame",
                    "-b:a",
                    "192k",
                    str(output_file),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        ensure_file_size_allowed(output_file)
    except subprocess.CalledProcessError as exc:
        cleanup_generated_media(temp_path)
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)

        if "Output file does not contain any stream" in detail:
            detail = "A midia informada nao possui trilha de audio para converter."

        raise HTTPException(
            status_code=400,
            detail=f"Nao foi possivel converter a midia para MP3 com FFmpeg: {detail}",
        )
    except HTTPException:
        cleanup_generated_media(temp_path)
        raise
    except Exception as exc:
        cleanup_generated_media(temp_path)
        raise HTTPException(
            status_code=400,
            detail=f"Nao foi possivel converter a midia para MP3: {exc}",
        )

    return GeneratedMediaFile(output_file, "audio/mpeg", temp_path)
