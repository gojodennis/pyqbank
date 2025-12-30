
import sys
import os
from pathlib import Path

# Add backend directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from datasets import load_dataset
from app.services.gemini_ocr import transcribe_image
from app.services.search_engine import add_documents
import tqdm

def ingest_dataset(limit=10):
    print(f"Loading Reja1/jee-neet-benchmark (streaming)... limit={limit}")
    ds = load_dataset("Reja1/jee-neet-benchmark", split="test", streaming=True, trust_remote_code=True)
    
    documents = []
    count = 0
    
    try:
        for item in tqdm.tqdm(ds):
            if count >= limit:
                break
            
            image = item.get('image')
            question_id = item.get('question_id', f"q_{count}")
            subject = item.get('subject', 'Unknown')
            exam_year = item.get('exam_year', 'Unknown')
            
            # Skip if no image
            if not image:
                continue
                
            print(f"Processing {question_id}...")
            
            # OCR with Gemini
            result = transcribe_image(image)
            
            if result.get('error'):
                print(f"Skipping {question_id}: {result['error']}")
                continue
                
            question_text = result.get('question_text', '')
            options = result.get('options', [])
            
            full_content = f"{question_text}\nOptions: {', '.join(options)}"
            
            if not question_text:
                continue
                
            doc = {
                "id": str(question_id),
                "content": full_content,
                "tags": f"{subject},{exam_year}",
                "year": str(exam_year),
                "subject": subject
            }
            
            documents.append(doc)
            count += 1
            
        print(f"Indexing {len(documents)} documents...")
        add_documents(documents)
        print("Done!")
        
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    qty = 5
    if len(sys.argv) > 1:
        qty = int(sys.argv[1])
    ingest_dataset(limit=qty)
