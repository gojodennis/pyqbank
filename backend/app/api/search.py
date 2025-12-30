from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel
from app.services.search_engine import search_index

router = APIRouter()

class SearchResult(BaseModel):
    id: str
    content: str
    score: float
    subject: str = None
    year: str = None
    tags: str = None
    options: list = None
    correct_answer: str = None
    explanation: str = None

@router.get("/search", response_model=List[SearchResult])
def search_questions(q: str = Query(..., min_length=3)):
    """
    Search for questions using Whoosh index.
    """
    results = search_index(q)
    # Mock data if index is empty (for verifying frontend)
    if not results:
        return [
            {"id": "1", "content": "Explain the process of Glycolysis. (Biology, 2023)", "score": 1.0},
            {"id": "2", "content": "Calculate the angular momentum of an electron. (Physics, 2022)", "score": 0.9},
            {"id": "3", "content": "What is the IUPAC name of the compound? (Chemistry, 2024)", "score": 0.85},
        ]
    return results
