from google import genai
from app.core.config import settings
from typing import Optional
import time
import random

# Initialize client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_explanation(question_text: str, options: list[str] = [], correct_answer: Optional[str] = None) -> str:
    """
    Generates an explanation for a given question using Google Gemini.
    Includes retry logic for rate limits.
    """
    model_name = "gemini-2.0-flash-lite-preview-02-05" 
    # Use reliable internal model ID if 2.5 is problematic, but the user wants 2.5-flash-lite
    # Previous logs showed 2.5-flash-lite working until quota hit.
    # However, to ensure success now, I will use "gemini-2.0-flash-lite-preview-02-05" which is the current "Flash Lite" reference or just "gemini-2.0-flash-lite".
    # Let's revert to "gemini-2.0-flash" or try "gemini-2.0-flash-lite-preview" if we want to be cutting edge.
    # SAFEST: "gemini-1.5-flash" - known good for production? No, user wanted 2.5.
    # The quota error earlier showed: `value: "gemini-2.5-flash-lite"`. So the ID is valid.
    model_name = "gemini-2.5-flash-lite"

    prompt = f"""
    Explain the following NEET/JEE question clearly.
    
    Question: {question_text}
    
    Options:
    {chr(10).join(f"- {opt}" for opt in options)}
    
    Correct Answer from Key: {correct_answer if correct_answer else "Not provided (deduce it)"}
    
    Task:
    1. Identify the correct option and explain WHY it is correct.
    2. Briefly explain why the other options are incorrect.
    3. State the key concept from NCERT (Physics/Chemistry/Biology) involved.
    """
    
    max_retries = 3
    base_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            # New SDK usage
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            is_rate_limit = "429" in error_str
            
            # If it's the last attempt, or not a rate limit error that we want to retry immediately
            if attempt == max_retries - 1 or not is_rate_limit:
                return f"Error generating explanation: {error_str}"
            
            # Calculate sleep time with exponential backoff and jitter
            sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
            print(f"Gemini API rate limit hit (Attempt {attempt+1}/{max_retries}). Retrying in {sleep_time:.2f}s...")
            time.sleep(sleep_time)

    return "Error: Failed to generate explanation after retries."
