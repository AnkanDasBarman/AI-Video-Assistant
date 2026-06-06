import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def seconds_to_mmss(seconds):
    try:
        seconds = float(seconds)
    except Exception:
        seconds = 0.0

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02d}:{seconds:02d}"


def search_visuals(video_id, query):
    video_folder = BASE_DIR / "data" / video_id

    index_path = video_folder / "visual_faiss.bin"
    metadata_path = video_folder / "visual_metadata.json"

    if not index_path.exists() or not metadata_path.exists():
        return {"error": "Video not found"}

    index = faiss.read_index(str(index_path))

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype(np.float32)

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        min(5, len(metadata))
    )

    results = []
    for position, idx in enumerate(indices[0]):
        if idx == -1 or idx >= len(metadata):
            continue

        item = metadata[idx]
        results.append({
            "timestamp": seconds_to_mmss(item.get("timestamp", 0)),
            "frame": item.get("frame"),
            "caption": item.get("caption"),
            "score": float(scores[0][position])
        })

    return results
