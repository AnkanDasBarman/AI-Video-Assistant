from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import os

from services.video_service import process_video

router = APIRouter()

UPLOAD_DIR = "backend/uploads"

@router.post("/upload-video")
async def upload_video(
    file: UploadFile = File(...)
):

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as f:

        content = await file.read()

        f.write(content)

    result = process_video(
        file_path,
        source="upload"
    )

    return result
