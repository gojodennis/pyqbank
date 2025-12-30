
# Dataset Usage Guide

This project is configured to work with the **JEE/NEET Benchmark Dataset** (`Reja1/jee-neet-benchmark`) from Hugging Face.

Since the dataset consists of images, we use a hybrid approach:
1.  **Metadata**: Downloaded directly to get Question ID, Subject, Year, and the Answer Key.
2.  **Images**: Downloaded on-the-fly and processed using **Gemini 2.0 Flash Exp** (OCR) to extract the Question Text and Options.
3.  **Indexing**: Processed data is stored in a local Whoosh index for fast searching.

## How to Ingest Data

We have created a robust, resumable ingestion script at `backend/scripts/ingest_manual.py`.

### Prerequisites
- Ensure your backend virtual environment is active.
- Ensure `GEMINI_API_KEY` is set in `.env` (or environment).

### Running the Ingestion

To start (or resume) ingestion, run:

```bash
cd backend
# Process the next 10 items
python scripts/ingest_manual.py 10
```

To process a larger batch (e.g., 50 items):

```bash
python scripts/ingest_manual.py 50
```

### Rate Limits & Resuming
The script uses the **Gemini 2.0 Flash Exp** model which has a free tier rate limit.
- If you hit a rate limit (429 Error), the script will automatically retry with exponential backoff.
- If it fails completely or you stop the script, **it is safe to run it again**.
- The script checks if a Question ID is already in the index and **skips it automatically**. This means you can just keep running the command to eventually process the entire dataset.

### Verifying Data
You can seed verifiable dummy data to test the search flow without waiting for OCR:

```bash
python scripts/seed_dummy_data.py
```
