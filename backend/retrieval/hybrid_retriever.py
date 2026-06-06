from backend.embeddings.search_embeddings import (
    search_video
)

from backend.vision.visual_search import (
    search_visual
)


def hybrid_search(
    query,
    audio_index,
    audio_metadata,
    visual_index,
    visual_metadata
):
    print("Hybrid Search - audio_index:", audio_index)
    print("Hybrid Search - audio_metadata:", audio_metadata)
    print("Hybrid Search - visual_index:", visual_index)
    print("Hybrid Search - visual_metadata:", visual_metadata)

    audio_results = search_video(
        query=query,
        index_path=audio_index,
        metadata_path=audio_metadata,
        top_k=5
    )

    visual_results = search_visual(
        query=query,
        index_file=visual_index,
        metadata_file=visual_metadata,
        top_k=3
    )

    return {
        "audio": audio_results,
        "visual": visual_results
    }
