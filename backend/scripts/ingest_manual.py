
import sys
import os
import json
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.gemini_ocr import transcribe_image
from app.services.search_engine import add_documents, document_exists

BASE_URL = "https://huggingface.co/datasets/Reja1/jee-neet-benchmark/resolve/main"

def download_metadata():
    if os.path.exists("metadata.jsonl"):
        print("Using cached metadata.jsonl")
        with open("metadata.jsonl", "r", encoding="utf-8") as f:
            return f.read().splitlines()

    print("Downloading metadata.jsonl...")
    url = f"{BASE_URL}/data/metadata.jsonl"
    resp = requests.get(url)
    resp.raise_for_status()
    
    with open("metadata.jsonl", "w", encoding="utf-8") as f:
        f.write(resp.text)
        
    return resp.text.splitlines()

import time

def ingest_manual(limit=10):
    lines = download_metadata()
    print(f"Found {len(lines)} items in metadata.")
    
    documents = []
    processed_count = 0
    
    for line in lines:
        if processed_count >= limit:
            break
            
        try:
            item = json.loads(line)
            question_id = item.get('question_id')
            
            # Check if already indexed
            if question_id and document_exists(str(question_id)):
                # print(f"Skipping {question_id} (already indexed)")
                continue

            # Rate limiting pause (reduced since we handle errors inside OCR now)
            time.sleep(2) 
            
            image_path = item.get('image_path') or item.get('file_name')
            
            # If image path not in item, maybe construct it?
            # Based on inspection, let's assume item has 'image_path' matching the repo structure.
            # If not, I'll print item keys to debug.
            
            if not image_path:
                print(f"No image path for item: {item.keys()}")
                continue
                
            # Construct image URL
            # image_path usually looks like 'images/...'
            image_url = f"{BASE_URL}/{image_path}"
            
            # Download image
            # print(f"Downloading image: {image_url}")
            img_resp = requests.get(image_url)
            if img_resp.status_code != 200:
                print(f"Failed to download {image_url}")
                continue
                
            image = Image.open(BytesIO(img_resp.content))
            
            question_id = item.get('question_id', f"q_{processed_count}")
            subject = item.get('subject', 'Unknown')
            exam_year = item.get('exam_year', 'Unknown')
            
            print(f"Processing {question_id} ({subject} {exam_year})...")
            
            # Gemini OCR
            ocr_result = transcribe_image(image)
            
            if ocr_result.get('error'):
                print(f"OCR Error: {ocr_result['error']}")
                time.sleep(5) # Backoff a bit more on error
                continue
                
            # Correct answer extraction from metadata (if available)
            correct_answer_meta = item.get('correct_answer')
            
            question_text = ocr_result.get('question_text', '')
            options = ocr_result.get('options', [])
            ocr_explanation = ocr_result.get('explanation', '')
            
            full_content = f"{question_text}\nOptions: {', '.join(options)}"
            
            doc = {
                "id": str(question_id),
                "content": full_content,
                "tags": f"{subject},{exam_year}",
                "year": str(exam_year),
                "subject": subject,
                "options": options,
                "correct_answer": correct_answer_meta,
                "explanation": ocr_explanation
            }
            
            # Add document immediately to index so we can resume if crash
            add_documents([doc])
            print(f"Indexed {question_id}")
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing item: {e}")
            

    print("Ingestion complete.")

if __name__ == "__main__":
    # Default to a small batch but allow running larger batches
    qty = 5
    if len(sys.argv) > 1:
        qty = int(sys.argv[1])
    # Pass a very large number if you want to index everything: `python ingest_manual.py 1000`
    ingest_manual(limit=qty)
