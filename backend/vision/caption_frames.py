import os
import json

from PIL import Image

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)


def clean_caption(text):

    if not text:
        return None

    words = text.split()

    if not words:
        return None

    unique_ratio = len(set(words)) / len(words)

    # If less than 80% of the words are unique, treat caption as repetitive/noisy
    if unique_ratio < 0.8:
        return None

    return text


def caption_frames(
    frames_folder,
    output_file
):

    MODEL_DIR = "models/blip"

    print("Loading BLIP model...")

    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base",
        cache_dir=MODEL_DIR
    )

    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base",
        cache_dir=MODEL_DIR
    )

    captions = []

    frame_files = sorted(
        [
            f
            for f in os.listdir(frames_folder)
            if f.endswith(".jpg")
        ]
    )

    for frame in frame_files:

        image_path = os.path.join(
            frames_folder,
            frame
        )

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = processor(
            image,
            return_tensors="pt"
        )

        output = model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=5
        )

        caption = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        caption = clean_caption(
            caption
        )

        if not caption:
            continue

        words = caption.split()

        if len(set(words)) <= 2:
            continue

        frame_number = int(
            frame.split("_")[1].split(".")[0]
        )

        timestamp = frame_number * 5

        captions.append({
            "frame": frame,
            "timestamp": timestamp,
            "caption": caption
        })

        print(
            f"{frame}: {caption}"
        )

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            captions,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nSaved captions to {output_file}"
    )

    return captions
