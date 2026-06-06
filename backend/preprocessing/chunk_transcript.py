import json
import os


def chunk_transcript(
    transcript_path,
    output_path,
    max_chars=500
):

    with open(
        transcript_path,
        "r",
        encoding="utf-8"
    ) as f:
        transcript = json.load(f)

    chunks = []

    current_text = ""
    start_time = None
    end_time = None

    for segment in transcript:

        text = segment["text"]

        if start_time is None:
            start_time = segment["start"]

        if len(current_text) + len(text) < max_chars or not current_text:

            current_text += " " + text
            end_time = segment["end"]

        else:

            chunks.append({
                "chunk_id": len(chunks),
                "start": start_time,
                "end": end_time,
                "text": current_text.strip()
            })

            current_text = text
            start_time = segment["start"]
            end_time = segment["end"]

    if current_text:

        chunks.append({
            "chunk_id": len(chunks),
            "start": start_time,
            "end": end_time,
            "text": current_text.strip()
        })

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with open(
        output_path,
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
        f"Created {len(chunks)} chunks"
    )

    return chunks
