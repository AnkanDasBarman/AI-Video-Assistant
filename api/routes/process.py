from fastapi import APIRouter
from pathlib import Path
import os

router = APIRouter()


def _find_latest_upload(upload_dir="backend/uploads"):
    p = Path(upload_dir)
    if not p.exists():
        return None

    files = [f for f in p.iterdir() if f.is_file() and f.suffix.lower() in {".mp4", ".mov", ".mkv"}]
    if not files:
        return None

    latest = max(files, key=lambda f: f.stat().st_mtime)
    return str(latest)


@router.post("/process-video")
def process_uploaded_video():

    from services.video_service import process_video

    video_path = _find_latest_upload()
    if not video_path:
        return {"status": "error", "message": "No uploaded video found in backend/uploads"}

    result = process_video(video_path)

    return result
