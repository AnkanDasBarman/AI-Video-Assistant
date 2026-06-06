import json
import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


def search_visual(
    query,
    index_file,
    metadata_file,
    top_k=3
):

    index_file = os.path.abspath(str(index_file))
    metadata_file = os.path.abspath(str(metadata_file))

    print(type(index_file))
    print(index_file)

    if not os.path.exists(index_file):
        raise FileNotFoundError(f"Visual index not found: {index_file}")

    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"Visual metadata not found: {metadata_file}")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    index = faiss.read_index(
        index_file
    )

    with open(
        metadata_file,
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
    )

    faiss.normalize_L2(
        query_embedding
    )

    scores, indices = index.search(
        query_embedding.astype(np.float32),
        top_k
    )

    results = []

    for idx, score in zip(
        indices[0],
        scores[0]
    ):

        if idx == -1:
            continue

        result = dict(metadata[idx])
        result["score"] = float(score)

        results.append(result)

    return results
