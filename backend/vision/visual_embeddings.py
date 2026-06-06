import json
import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


def build_visual_index(
    captions_file,
    index_file,
    metadata_file
):

    captions_file = os.path.abspath(str(captions_file))
    index_file = os.path.abspath(str(index_file))
    metadata_file = os.path.abspath(str(metadata_file))

    print("Loading embedding model...")
    print("INDEX FILE:", index_file)
    print("METADATA FILE:", metadata_file)

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    with open(
        captions_file,
        "r",
        encoding="utf-8"
    ) as f:

        captions = json.load(f)

    texts = [
        item["caption"]
        for item in captions
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype(np.float32)
    # Ensure embeddings is 2D (num_vectors, dim) for FAISS normalization
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)
    faiss.normalize_L2(
        embeddings
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(embeddings)

    # IMPORTANT
    print(type(index_file))
    print(index_file)
    faiss.write_index(
        index,
        str(index_file)
    )

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            captions,
            f,
            indent=4
        )

    print("Visual index created.")
