from pathlib import Path

import ffmpeg
from moviepy import VideoFileClip


def extract_audio(video_path, output_audio_path):
    """Extract audio from `video_path` and save it to `output_audio_path`."""
    video_path = Path(video_path)
    output_audio_path = Path(output_audio_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    output_audio_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        (
            ffmpeg
            .input(str(video_path))
            .output(str(output_audio_path), acodec="mp3", vn=None)
            .overwrite_output()
            .run(quiet=True)
        )
    except FileNotFoundError:
        # Fallback when ffmpeg executable is not available in PATH.
        try:
            with VideoFileClip(str(video_path)) as clip:
                if clip.audio is None:
                    raise RuntimeError("No audio stream found in the input video.")
                clip.audio.write_audiofile(str(output_audio_path), logger=None)
        except Exception as exc:
            raise RuntimeError(
                "Audio extraction failed. ffmpeg executable was not found and "
                f"moviepy fallback also failed: {exc}"
            ) from exc
    except ffmpeg.Error as exc:
        stderr = exc.stderr.decode("utf-8", errors="ignore") if exc.stderr else str(exc)
        raise RuntimeError(f"Audio extraction failed: {stderr}") from exc

    return str(output_audio_path)
