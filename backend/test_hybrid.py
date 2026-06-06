from retrieval.hybrid_retriever import (
    hybrid_search
)

results = hybrid_search(
    query="machine learning",
    audio_index="vector_db/faiss_index.bin",
    audio_metadata="vector_db/metadata.json",
    visual_index="visual_data/visual_faiss.bin",
    visual_metadata="visual_data/visual_metadata.json"
)

print(results)
