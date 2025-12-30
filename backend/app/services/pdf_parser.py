import re
import spacy
from typing import List, Dict, Optional
from pydantic import BaseModel

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class ParsedQuestion(BaseModel):
    id: Optional[str] = None
    text: str
    options: List[str] = []
    subject: Optional[str] = None
    tags: List[str] = []

def extract_text_from_pdf(reader) -> str:
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def clean_text(text: str) -> str:
    # Remove header/footer noise (simple heuristic)
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if len(line.strip()) > 3] # Remove very short lines
    return " ".join(cleaned_lines)

def parse_questions_from_text(text: str) -> List[ParsedQuestion]:
    """
    Heuristic parser for standard exam papers.
    Assumes questions start with a number followed by dot or parenthesis (e.g., "1.", "1)").
    """
    # Regex for Question Start: "1." or "1)" at start of line or after newline
    question_pattern = re.compile(r'(?:\n|^)(\d+)[\.\)]\s+')
    
    questions = []
    splits = list(question_pattern.finditer(text))
    
    if not splits:
        return []

    for i in range(len(splits)):
        start = splits[i].start()
        end = splits[i+1].start() if i + 1 < len(splits) else len(text)
        
        # Extract full question block
        q_block = text[start:end].strip()
        
        # separate question number
        match = question_pattern.match(q_block) or question_pattern.search(q_block)
        if match:
            q_num = match.group(1)
            content = q_block[match.end():].strip()
        else:
            continue

        # Basic Option Extraction (A., B., C., D. or (a), (b)...)
        # simplistic splitting for now
        # In a real scenario, this needs robust regex for options
        
        # NLP Tagging
        doc = nlp(content[:200]) # Analyze first 200 chars for topics
        tags = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "PRODUCT", "WORK_OF_ART", "PERSON")]
        
        # Subject heuristic (very naive, usually passed via file metadata)
        subject = "General"
        if "physics" in content.lower(): subject = "Physics"
        elif "chemistry" in content.lower(): subject = "Chemistry"
        elif "biology" in content.lower(): subject = "Biology"

        questions.append(ParsedQuestion(
            id=str(q_num),
            text=content,
            tags=tags,
            subject=subject
        ))
        
    return questions
