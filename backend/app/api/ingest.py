from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import shutil
import os
import PyPDF2
from app.services.pdf_parser import extract_text_from_pdf, parse_questions_from_text
from app.services.search_engine import add_documents

router = APIRouter()

UPLOAD_DIR = "uploaded_pdfs"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF, parse it, and index the questions.
    """
    try:
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        # Parse PDF
        with open(file_location, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = extract_text_from_pdf(reader)
            
        questions = parse_questions_from_text(text)
        
        # Prepare for Indexing
        documents = []
        for q in questions:
            documents.append({
                "id": f"{file.filename}_{q.id}",
                "content": q.text,
                "tags": ",".join(q.tags),
                "year": "2023", # Placeholder, would come from metadata
                "subject": q.subject
            })
            
        # Index
        add_documents(documents)
        
        return {"filename": file.filename, "questions_processed": len(questions)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
