
from google import genai
import os
import json
import time
import random
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client
client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.0-flash-exp" 

def transcribe_image(image: Image.Image) -> dict:
    """
    Uses Gemini to extract text, options, and metadata from a question image.
    """
    if not client:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    prompt = """
    Analyze this image of a multiple-choice question from a NEET/JEE exam.
    Extract the following fields and return ONLY a valid JSON object:
    {
        "question_text": "The full text of the question",
        "options": ["Option A text", "Option B text", ...],
        "correct_answer": "The correct answer option/text if marked or visible, else null",
        "explanation": "Any solution or explanation text visible, else null"
    }
    If the image is not a question or unreadable, return {"error": "unreadable"}.
    """
    
    max_retries = 3
    base_delay = 2

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[prompt, image]
            )
            # Clean response to get just JSON
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()
                
            return json.loads(text)
        except Exception as e:
            error_str = str(e)
            is_rate_limit = "429" in error_str
            
            if attempt == max_retries - 1 or not is_rate_limit:
                 print(f"Error transforming image: {e}")
                 # 'response' might not exist if assignment failed
                 return {"error": str(e), "raw": ""}
            
            sleep_time = (base_delay * (3 ** attempt)) + random.uniform(5, 10)
            print(f"Gemini OCR rate limit hit (Attempt {attempt+1}/{max_retries}). Retrying in {sleep_time:.2f}s...")
            time.sleep(sleep_time)
            
    return {"error": "Failed after retries"}


