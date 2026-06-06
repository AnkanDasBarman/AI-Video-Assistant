from fastapi import APIRouter

from models.question_request import QuestionRequest
from services.qa_service import ask_question

router = APIRouter()

@router.post("/ask-question")
def ask(
    request: QuestionRequest
):
    result = ask_question(
        request.video_id,
        request.question
    )

    return {
        "video_id": request.video_id,
        "question": request.question,
        **result
    }
