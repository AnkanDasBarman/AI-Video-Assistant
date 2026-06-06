from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import json


class VideoRequest(BaseModel):
    video_id: str


router = APIRouter()


def format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def extract_topic(text: str, max_words: int = 8) -> str:
    if not text:
        return "(no topic)"

    # Try to get the first sentence-ish chunk
    first_sentence = text.split(".")[0]
    words = first_sentence.strip().split()
    topic = " ".join(words[:max_words])
    # Clean up trailing commas or colons
    topic = topic.strip().rstrip(',:;')
    if len(words) > max_words:
        topic += "..."
    return topic


@router.post("/", response_model=List[Dict])
def video_timeline(req: VideoRequest):
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    video_path = os.path.join(data_dir, req.video_id, "metadata.json")

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video metadata not found")

    with open(video_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    timeline = []
    for chunk in chunks:
        # Support both legacy 'content' and new 'text' keys
        text = chunk.get("text") or chunk.get("content") or ""
        start = float(chunk.get("start", 0))
        end = float(chunk.get("end", start))

        timeline.append({
            "start": format_time(start),
            "end": format_time(end),
            "topic": extract_topic(text)
        })

    return timeline
