from fastapi import APIRouter

from src.modules.media_tools.schemas import MediaUrlRequest
from src.modules.media_tools.service import download_audio_mp3, download_video, get_media_info

router = APIRouter()


@router.post("/info")
def media_info_route(payload: MediaUrlRequest):
    return get_media_info(payload.url)


@router.post("/download-video")
def download_video_route(payload: MediaUrlRequest):
    return download_video(payload.url)


@router.post("/download-audio")
def download_audio_route(payload: MediaUrlRequest):
    return download_audio_mp3(payload.url)
