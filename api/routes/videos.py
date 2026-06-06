from fastapi import APIRouter

from services.metadata_service import get_all_videos

router = APIRouter()

@router.get("/videos")
def list_videos():
    return get_all_videos()
