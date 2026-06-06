from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.video_search_service import search_video

router = APIRouter()


class SearchRequest(BaseModel):
    video_id: str
    query: str


@router.post("/video-search")
def video_search(request: SearchRequest):
    return search_video(
        request.video_id,
        request.query
    )
