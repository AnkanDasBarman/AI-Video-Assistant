from pathlib import Path
import os

from dotenv import load_dotenv

from backend.retrieval.hybrid_retriever import hybrid_search

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "backend" / ".env")


def ask_question(video_id, question):
    data_root = BASE_DIR / "backend" / "data" / video_id
    audio_index = data_root / "faiss_index.bin"
    audio_metadata = data_root / "metadata.json"
    visual_index = data_root / "visual_faiss.bin"
    visual_metadata = data_root / "visual_metadata.json"

    # Diagnostics: show which files we're about to read
    try:
        print("QA_SERVICE: audio_index=", str(audio_index.resolve()))
        print("QA_SERVICE: audio_metadata=", str(audio_metadata.resolve()))
        print("QA_SERVICE: visual_index=", str(visual_index.resolve()))
        print("QA_SERVICE: visual_metadata=", str(visual_metadata.resolve()))
        print("QA_SERVICE: audio_index exists:", audio_index.exists())
        print("QA_SERVICE: audio_metadata exists:", audio_metadata.exists())
        print("QA_SERVICE: visual_index exists:", visual_index.exists())
        print("QA_SERVICE: visual_metadata exists:", visual_metadata.exists())
    except Exception as e:
        print("QA_SERVICE: diagnostic error:", e)

    results = hybrid_search(
        query=question,
        audio_index=audio_index,
        audio_metadata=audio_metadata,
        visual_index=visual_index,
        visual_metadata=visual_metadata
    )

    # Guard: if GROQ API key missing, return retrieved contexts for debugging
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return {
            "question": question,
            "answer": None,
            "audio_sources": len(results.get("audio", [])),
            "visual_sources": len(results.get("visual", [])),
            "warning": "GROQ_API_KEY not set; cannot call LLM.",
            "retrieved": results
        }

    # Import VideoQA lazily; handle missing `groq` package gracefully
    try:
        from backend.qa.rag_pipeline import VideoQA
    except Exception as e:
        return {
            "question": question,
            "answer": None,
            "audio_sources": len(results.get("audio", [])),
            "visual_sources": len(results.get("visual", [])),
            "warning": f"Failed to import VideoQA: {e}",
            "retrieved": results
        }

    qa = VideoQA(
        api_key=groq_key
    )

    answer = qa.answer_question(
        question,
        results
    )

    return {
        "question": question,
        "answer": answer,
        "audio_sources": len(results["audio"]),
        "visual_sources": len(results["visual"])
    }
