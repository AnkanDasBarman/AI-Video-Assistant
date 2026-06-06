from video_processing.extract_frames import extract_frames
from video_processing.extract_audio import extract_audio
from transcription.whisper_transcriber import transcribe_audio
from preprocessing.chunk_transcript import chunk_transcript
from embeddings.create_embeddings import build_vector_database
from vision.caption_frames import caption_frames
from vision.visual_embeddings import build_visual_index
from retrieval.hybrid_retriever import hybrid_search
from qa.rag_pipeline import VideoQA
from services.ingestion_service import ingest
from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

FRAMES_OUTPUT = BASE_DIR / "extracted_frames"

AUDIO_OUTPUT = BASE_DIR / "extracted_audio" / "audio.mp3"

TRANSCRIPT_OUTPUT = BASE_DIR / "transcripts" / "transcript.json"

CHUNK_OUTPUT = BASE_DIR / "transcripts" / "chunked_transcript.json"

INDEX_PATH = BASE_DIR / "vector_db" / "faiss_index.bin"

METADATA_PATH = BASE_DIR / "vector_db" / "metadata.json"
VISUAL_CAPTIONS_PATH = BASE_DIR / "visual_data" / "captions.json"
VISUAL_INDEX_PATH = BASE_DIR / "visual_data" / "visual_faiss.bin"
VISUAL_METADATA_PATH = BASE_DIR / "visual_data" / "visual_metadata.json"


def process_video(video_path):
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    print(f"\nProcessing video: {video_path}")

    frame_count = extract_frames(
        video_path=video_path,
        output_folder=FRAMES_OUTPUT,
        interval=5
    )
    print(f"Extracted {frame_count} frames to: {FRAMES_OUTPUT}")

    audio_path = extract_audio(
        video_path=video_path,
        output_audio_path=AUDIO_OUTPUT
    )
    print(f"Extracted audio to: {audio_path}")

    transcribe_audio(
        audio_path=AUDIO_OUTPUT,
        output_json=TRANSCRIPT_OUTPUT
    )

    chunks = chunk_transcript(
        transcript_path=TRANSCRIPT_OUTPUT,
        output_path=CHUNK_OUTPUT,
        max_chars=500
    )

    build_vector_database(
        chunk_file=CHUNK_OUTPUT,
        index_output=INDEX_PATH,
        metadata_output=METADATA_PATH
    )

    caption_frames(
        frames_folder=FRAMES_OUTPUT,
        output_file=VISUAL_CAPTIONS_PATH
    )

    build_visual_index(
        captions_file=VISUAL_CAPTIONS_PATH,
        index_file=VISUAL_INDEX_PATH,
        metadata_file=VISUAL_METADATA_PATH
    )

    return {
        "chunks": len(chunks),
        "status": "success"
    }


def ask_question(question, top_k=7):
    results = hybrid_search(
        query=question,
        audio_index=INDEX_PATH,
        audio_metadata=METADATA_PATH,
        visual_index=VISUAL_INDEX_PATH,
        visual_metadata=VISUAL_METADATA_PATH
    )

    qa = VideoQA(
        api_key=os.getenv("GROQ_API_KEY")
    )

    answer = qa.answer_question(
        question=question,
        retrieved_context=results
    )

    return {
        "answer": answer,
        "results": results
    }


if __name__ == "__main__":
    source = input("Enter video path or URL: ").strip()
    if not source:
        source = str(BASE_DIR / "uploads" / "Sample2.mp4")

    video_path = ingest(source)
    process_info = process_video(video_path)
    print(f"\nVideo processing status: {process_info}")

    question = input("\nAsk a question: ").strip()
    if not question:
        question = "What does the speaker say about sustainable development?"

    qa_result = ask_question(question)
    results = qa_result["results"]

    print("\nSEARCH RESULTS:\n")
    for result in results.get("audio", []):
        print(result)

    print("\nVISUAL RESULTS:\n")
    for result in results.get("visual", []):
        print(result)

    print("\nANSWER:\n")
    print(qa_result["answer"])
