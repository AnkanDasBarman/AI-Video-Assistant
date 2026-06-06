from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os, json

router = APIRouter()

@router.get("/video/{video_id}")
def stream_video(video_id: str):
    """Serve a video file based on video_id.
    Looks up the video metadata to find the original title, then serves the corresponding file from uploads.
    """
    uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
    # Load metadata to map video_id to filename (title)
    metadata_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../metadata/videos.json"))
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            videos = json.load(f)
    except Exception:
        videos = []
    filename = None
    for entry in videos:
        if entry.get("video_id") == video_id:
            # Use title as filename (may contain spaces)
            title = entry.get("title", "")
            # Attempt common extensions
            for ext in [".mp4", ".webm", ".ogg"]:
                candidate = os.path.join(uploads_dir, f"{title}{ext}")
                if os.path.isfile(candidate):
                    filename = candidate
                    break
            if filename:
                break
    # Fallback: any file containing video_id
    if not filename:
        for fname in os.listdir(uploads_dir):
            if video_id.lower() in fname.lower() and fname.lower().endswith(('.mp4', '.webm', '.ogg')):
                filename = os.path.join(uploads_dir, fname)
                break
    if filename and os.path.isfile(filename):
        return FileResponse(filename, media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Video not found")


