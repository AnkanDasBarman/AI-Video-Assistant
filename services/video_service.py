import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

from services.metadata_service import save_video_metadata



def process_video(video_path, source="upload"):

    # Import heavy backend modules lazily to avoid import-time failures
    from backend.video_processing.extract_frames import extract_frames
    from backend.video_processing.extract_audio import extract_audio
    from backend.transcription.whisper_transcriber import transcribe_audio
    from backend.preprocessing.chunk_transcript import chunk_transcript
    from backend.embeddings.create_embeddings import build_vector_database
    from backend.vision.caption_frames import caption_frames
    from backend.vision.visual_embeddings import build_visual_index

    root = BASE_DIR
    backend_root = root / "backend"

    # Create a per-video data folder
    video_id = str(uuid.uuid4())[:8]
    video_folder = backend_root / "data" / video_id
    video_folder.mkdir(parents=True, exist_ok=True)

    # Use per-video asset paths to avoid cross-video overwrites
    frames_dir = video_folder / "frames"
    audio_file = video_folder / "audio.mp3"

    # Per-video artifact files
    transcript_file = video_folder / "transcript.json"
    chunk_file = video_folder / "chunked_transcript.json"
    index_file = video_folder / "faiss_index.bin"
    metadata_file = video_folder / "metadata.json"
    captions_file = video_folder / "captions.json"
    visual_index = video_folder / "visual_faiss.bin"
    visual_metadata = video_folder / "visual_metadata.json"

    # Diagnostics: print the paths being used so we can verify no mismatches
    try:
        print("PROCESS_VIDEO: video_path=", video_path)
        print("PROCESS_VIDEO: video_id=", video_id)
        print("PROCESS_VIDEO: video_folder=", str(video_folder.resolve()))
        print("PROCESS_VIDEO: frames_dir=", str(frames_dir.resolve()))
        print("PROCESS_VIDEO: audio_file=", str(audio_file.resolve()))
        print("PROCESS_VIDEO: transcript_file=", str(transcript_file.resolve()))
        print("PROCESS_VIDEO: chunk_file=", str(chunk_file.resolve()))
        print("PROCESS_VIDEO: index_file=", str(index_file.resolve()))
        print("PROCESS_VIDEO: metadata_file=", str(metadata_file.resolve()))
        print("PROCESS_VIDEO: captions_file=", str(captions_file.resolve()))
        print("PROCESS_VIDEO: visual_index=", str(visual_index.resolve()))
        print("PROCESS_VIDEO: visual_metadata=", str(visual_metadata.resolve()))
    except Exception as e:
        print("PROCESS_VIDEO: diagnostic path resolution error:", e)

    frame_count = extract_frames(
        video_path,
        frames_dir,
        interval=5
    )

    extract_audio(
        video_path,
        audio_file
    )

    transcribe_audio(
        audio_file,
        transcript_file
    )

    chunks = chunk_transcript(
        transcript_file,
        chunk_file
    )

    build_vector_database(
        chunk_file,
        index_file,
        metadata_file
    )

    caption_frames(
        frames_dir,
        captions_file
    )

    build_visual_index(
        captions_file,
        visual_index,
        visual_metadata
    )

    result = {
        "status": "success",
        "video_id": video_id,
        "title": Path(video_path).stem,
        "source": source,
        "frames": frame_count,
        "chunks": len(chunks)
    }

    # Save metadata
    metadata = {
        "video_id": video_id,
        "title": Path(video_path).stem,
        "source": source,
        "frames": frame_count,
        "chunks": len(chunks)
    }
    save_video_metadata(metadata)

    return result
