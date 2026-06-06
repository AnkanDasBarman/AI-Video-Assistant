import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VIDEOS_FILE = (
    BASE_DIR
    / "backend"
    / "metadata"
    / "videos.json"
)

def video_identity(video_data):
    return (
        video_data.get("title"),
        video_data.get("source")
    )

def dedupe_videos(videos):
    unique = {}

    for video in videos:
        unique[video_identity(video)] = video

    return list(unique.values())

def save_video_metadata(video_data):

    if not VIDEOS_FILE.exists():
        VIDEOS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(VIDEOS_FILE, "w") as f:
            json.dump([], f)

    with open(VIDEOS_FILE, "r") as f:
        videos = json.load(f)

    duplicate = video_identity(video_data) in {
        video_identity(video)
        for video in videos
    }

    if duplicate:
        return

    videos.append(video_data)

    with open(VIDEOS_FILE, "w") as f:
        json.dump(
            videos,
            f,
            indent=4
        )

def get_all_videos():

    if not VIDEOS_FILE.exists():
        return []

    with open(VIDEOS_FILE, "r") as f:
        return dedupe_videos(json.load(f))
