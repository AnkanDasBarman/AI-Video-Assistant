import json
from pathlib import Path

from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent


def seconds_to_mmss(seconds):
    try:
        seconds = float(seconds)
    except Exception:
        seconds = 0.0

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02d}:{seconds:02d}"


def generate_highlights(video_id):
    video_folder = BASE_DIR / "data" / video_id
    chunk_file = video_folder / "chunked_transcript.json"

    if not chunk_file.exists():
        return {"error": "Video not found"}

    with open(chunk_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        return {
            "video_id": video_id,
            "highlights": []
        }

    if len(chunks) >= 3:
        selected = [
            chunks[0],
            chunks[len(chunks) // 2],
            chunks[-1]
        ]
    else:
        selected = chunks

    client = Groq()
    highlights = []

    for chunk in selected:
        text = chunk.get("text", "")[:1000]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
                    Generate a short topic title.

                    Maximum 6 words.

                    Examples:

                    Introduction to AI
                    Machine Learning Basics
                    Deep Learning Overview

                    Return only title.
                    """
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        title = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        highlights.append({
            "timestamp": seconds_to_mmss(chunk.get("start", 0)),
            "topic": title
        })

    return {
        "video_id": video_id,
        "highlights": highlights
    }
