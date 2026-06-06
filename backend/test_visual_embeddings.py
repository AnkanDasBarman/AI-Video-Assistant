from vision.visual_embeddings import (
    build_visual_index
)

build_visual_index(
    captions_file="visual_data/captions.json",
    index_file="visual_data/visual_faiss.bin",
    metadata_file="visual_data/visual_metadata.json"
)
