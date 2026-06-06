import json
import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


def build_vector_database(
    chunk_file,
    index_output,
    metadata_output
):
    chunk_file = os.path.abspath(str(chunk_file))
    index_output = os.path.abspath(str(index_output))
    metadata_output = os.path.abspath(str(metadata_output))

    print("Loading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    with open(
        chunk_file,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    if not texts:
        raise ValueError("No transcript chunks found for embedding.")

    print(
        f"Generating embeddings for {len(texts)} chunks..."
    )

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    ).astype(np.float32)

    # Cosine similarity with FAISS: normalize vectors + inner product.
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    os.makedirs(
        os.path.dirname(index_output),
        exist_ok=True
    )

    faiss.write_index(
        index,
        index_output
    )

    with open(
        metadata_output,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Saved FAISS index to {index_output}"
    )

    print(
        f"Saved metadata to {metadata_output}"
    )
