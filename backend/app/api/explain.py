from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import generate_explanation

router = APIRouter()

class ExplainRequest(BaseModel):
    question_text: str
    question_id: str
    options: list[str] = []
    correct_answer: str = None

class ExplainResponse(BaseModel):
    explanation: str

@router.post("/explain", response_model=ExplainResponse)
async def explain_question(request: ExplainRequest):
    """
    Get an AI-generated explanation for a specific question.
    """
    try:
        explanation = generate_explanation(
            request.question_text, 
            options=request.options, 
            correct_answer=request.correct_answer
        )
        return {"explanation": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
