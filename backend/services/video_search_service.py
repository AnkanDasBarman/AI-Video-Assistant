import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

model = SentenceTransformer("all-MiniLM-L6-v2")


def search_video(video_id: str, query: str, top_k: int = 5):
    video_folder = BASE_DIR / "data" / video_id

    index_path = video_folder / "faiss_index.bin"
    metadata_path = video_folder / "metadata.json"

    if not index_path.exists() or not metadata_path.exists():
        return {"error": "Video not found"}

    index = faiss.read_index(str(index_path))

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Encode and normalize query
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype(np.float32)

    faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, min(top_k, len(metadata)))

    results = []

    for pos, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        if idx >= len(metadata):
            continue

        chunk = metadata[idx]
        text = chunk.get("text") or chunk.get("content") or ""

        def seconds_to_mmss(s):
            try:
                s = float(s)
            except Exception:
                s = 0.0
            minutes = int(s // 60)
            seconds = int(s % 60)
            return f"{minutes:02d}:{seconds:02d}"

        results.append({
            "start": seconds_to_mmss(chunk.get("start", 0)),
            "end": seconds_to_mmss(chunk.get("end", chunk.get("start", 0))),
            "text": text,
            "score": float(distances[0][pos])
        })

    return results
