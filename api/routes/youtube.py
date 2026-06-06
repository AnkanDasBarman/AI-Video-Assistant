from fastapi import APIRouter
from pathlib import Path

from schemas.youtube_schema import YoutubeRequest
from services.youtube_service import download_youtube_video
from services.video_service import process_video

router = APIRouter()

@router.post("/upload-url")
def upload_url(data: YoutubeRequest):
    """Download YouTube video and process it in one step"""

    # Step 1: Download from YouTube
    video_path = download_youtube_video(
        data.url,
        output_dir="backend/uploads"
    )

    # Step 2: Process the downloaded video (process_video generates its own video_id)
    result = process_video(video_path, source="youtube")

    return result
