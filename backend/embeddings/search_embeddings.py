import json
import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


def search_video(
    query,
    index_path,
    metadata_path,
    top_k=3
):
    index_path = os.path.abspath(str(index_path))
    metadata_path = os.path.abspath(str(metadata_path))

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    index = faiss.read_index(
        index_path
    )

    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    top_k = min(top_k, len(metadata))
    if top_k <= 0:
        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype(np.float32)

    faiss.normalize_L2(
        query_embedding
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx, score in zip(indices[0], distances[0]):
        if idx == -1:
            continue

        if idx < len(metadata):
            result = dict(metadata[idx])
            result["score"] = float(score)
            results.append(result)

    return results
