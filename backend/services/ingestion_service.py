import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
import yt_dlp


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"


def _timestamp_dir() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = UPLOAD_DIR / stamp
    target.mkdir(parents=True, exist_ok=True)
    return target


def _safe_stem(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in name)
    cleaned = cleaned.strip("_")
    return cleaned or "video"


def download_youtube(url):
    target_dir = _timestamp_dir()

    ydl_opts = {
        "outtmpl": str(target_dir / "%(title)s.%(ext)s"),
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info)

    candidate = Path(video_path)
    if candidate.suffix.lower() != ".mp4":
        merged = candidate.with_suffix(".mp4")
        if merged.exists():
            candidate = merged

    return str(candidate.resolve())


def download_video_url(url):
    target_dir = _timestamp_dir()

    parsed = urlparse(url)
    raw_name = Path(parsed.path).name or "downloaded.mp4"
    stem = _safe_stem(Path(raw_name).stem)
    output_path = target_dir / f"{stem}.mp4"

    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return str(output_path.resolve())


def ingest(source):
    source = str(source).strip()

    if os.path.exists(source):
        return str(Path(source).resolve())

    source_lower = source.lower()

    if any(host in source_lower for host in ["youtube.com", "youtu.be", "vimeo.com"]):
        return download_youtube(source)

    if source_lower.endswith(".mp4") or source_lower.startswith("http"):
        return download_video_url(source)

    raise ValueError("Unsupported source. Provide local path, YouTube/Vimeo URL, or direct video URL.")
