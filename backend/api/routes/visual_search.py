from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.visual_search_service import search_visuals

router = APIRouter()


class VisualSearchRequest(BaseModel):
    video_id: str
    query: str


@router.post("/visual-search")
def visual_search(request: VisualSearchRequest):
    return search_visuals(
        request.video_id,
        request.query
    )
