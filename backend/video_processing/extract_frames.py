from pathlib import Path

import cv2


def extract_frames(video_path, output_folder, interval=1):
    """
    Extract one frame every `interval` seconds from `video_path`.

    Returns the number of frames written.
    """
    if interval <= 0:
        raise ValueError("interval must be greater than 0")

    video_path = Path(video_path)
    output_folder = Path(output_folder)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    output_folder.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        cap.release()
        raise RuntimeError("Could not determine video FPS")

    frame_step = max(1, int(round(fps * interval)))
    frame_index = 0
    saved_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        if frame_index % frame_step == 0:
            output_path = output_folder / f"frame_{saved_count:05d}.jpg"
            cv2.imwrite(str(output_path), frame)
            saved_count += 1

        frame_index += 1

    cap.release()
    return saved_count
