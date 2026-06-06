import yt_dlp
from pathlib import Path

def download_youtube_video(url, output_dir="backend/uploads"):

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "best[ext=mp4]",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "quiet": False,
        "no_warnings": False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename
