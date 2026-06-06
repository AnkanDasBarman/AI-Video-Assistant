import json
from pathlib import Path


def _slug(name: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in name)
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "video"


def load_registry(registry_path):
    registry_path = Path(registry_path)
    if not registry_path.exists():
        return {}
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry_path, registry):
    registry_path = Path(registry_path)
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)


def get_video_id(video_path):
    return _slug(Path(video_path).stem)


def build_paths(memory_root, video_id):
    root = Path(memory_root) / video_id
    return {
        "root": root,
        "frames": root / "frames",
        "audio": root / "audio.mp3",
        "transcript": root / "transcript.json",
        "chunks": root / "chunked_transcript.json",
        "index": root / "faiss_index.bin",
        "metadata": root / "metadata.json",
    }


def memory_exists(paths):
    required = ["audio", "transcript", "chunks", "index", "metadata"]
    return all(Path(paths[key]).exists() for key in required)
