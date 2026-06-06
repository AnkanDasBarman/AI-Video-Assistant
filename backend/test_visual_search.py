from vision.visual_search import search_visual

results = search_visual(
    query="machine learning",
    index_file="visual_data/visual_faiss.bin",
    metadata_file="visual_data/visual_metadata.json"
)

for r in results:
    print(r)
