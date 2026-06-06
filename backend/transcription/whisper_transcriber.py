from faster_whisper import WhisperModel
import json
import os


def transcribe_audio(audio_path, output_json):

    print("Loading Whisper model...")

    try:
        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )
    except Exception as exc:
        raise RuntimeError(
            "Failed to load Whisper model. On first run, faster-whisper needs "
            "internet access to download model weights."
        ) from exc

    print("Transcribing audio...")

    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

    transcript = []

    for segment in segments:

        transcript.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })

    os.makedirs(
        os.path.dirname(output_json),
        exist_ok=True
    )

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(
            transcript,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Transcript saved to {output_json}")

    return transcript
