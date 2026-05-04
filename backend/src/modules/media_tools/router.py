from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from src.modules.media_tools.schemas import MediaUrlRequest
from src.modules.media_tools.service import (
    cleanup_generated_media,
    download_audio_mp3,
    download_video,
    get_media_info,
)

router = APIRouter()


@router.post("/info")
def media_info_route(payload: MediaUrlRequest):
    return get_media_info(payload.url)


@router.post("/download-video")
def download_video_route(payload: MediaUrlRequest):
    media_file = download_video(payload.url)
    return FileResponse(
        media_file.path,
        media_type=media_file.mime_type,
        filename=media_file.path.name,
        background=BackgroundTask(cleanup_generated_media, media_file.cleanup_dir),
    )


@router.post("/download-audio")
def download_audio_route(payload: MediaUrlRequest):
    media_file = download_audio_mp3(payload.url)
    return FileResponse(
        media_file.path,
        media_type=media_file.mime_type,
        filename=media_file.path.name,
        background=BackgroundTask(cleanup_generated_media, media_file.cleanup_dir),
    )
