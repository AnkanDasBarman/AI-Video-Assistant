from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def ask_question(question: str):
    return {
        "question": question,
        "answer": "QA endpoint placeholder"
    }
