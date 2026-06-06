from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.video_highlight_service import generate_highlights

router = APIRouter()


class HighlightRequest(BaseModel):
    video_id: str


@router.post("/video-highlights")
def video_highlights(request: HighlightRequest):
    return generate_highlights(
        request.video_id
    )
