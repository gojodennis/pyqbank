import os
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD, STORED
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin

INDEX_DIR = "indexdir"

def get_schema():
    return Schema(
        id=ID(stored=True, unique=True),
        content=TEXT(stored=True),
        tags=KEYWORD(stored=True, scorable=True),
        year=ID(stored=True),
        subject=ID(stored=True),
        options=STORED,
        correct_answer=STORED,
        explanation=STORED
    )

def create_index():
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
    
    # Initialize index
    create_in(INDEX_DIR, get_schema())

def add_documents(documents: list):
    """
    documents: List of dicts with keys matching schema
    """
    if not exists_in(INDEX_DIR):
        create_index()
    
    ix = open_dir(INDEX_DIR)
    writer = ix.writer()
    
    for doc in documents:
        writer.add_document(**doc)
    
    writer.commit()


def document_exists(doc_id):
    if not exists_in(INDEX_DIR):
        return False
    ix = open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        # Check if ID exists
        docnum = searcher.document_number(id=str(doc_id))
        return docnum is not None

def search_index(query_str: str, limit: int = 10):
    if not exists_in(INDEX_DIR):
        return []
        
    ix = open_dir(INDEX_DIR)
    with ix.searcher() as searcher:
        # Search efficiently across content, tags, subject, and year
        parser = MultifieldParser(["content", "tags", "subject", "year"], ix.schema)
        parser.add_plugin(FuzzyTermPlugin())
        
        try:
            # 1. Exact/Standard Search
            query = parser.parse(query_str)
            results = searcher.search(query, limit=limit)
            
            # 2. Results found? Return them.
            if len(results) > 0:
                 return [{"id": r["id"], "content": r["content"], "score": r.score, "subject": r.get("subject"), "year": r.get("year"), "tags": r.get("tags"), "options": r.get("options"), "correct_answer": r.get("correct_answer"), "explanation": r.get("explanation")} for r in results]

            # 3. No results? Try Fuzzy Search (Typo Tolerance)
            # Append ~1 (edit distance 1) to terms.
            terms = query_str.split()
            # Only apply fuzziness to terms longer than 3 chars to avoid noise
            fuzzy_terms = [f"{t}~1" if len(t) > 3 and t.isalnum() else t for t in terms]
            fuzzy_query_str = " ".join(fuzzy_terms)
            
            fuzzy_query = parser.parse(fuzzy_query_str)
            results = searcher.search(fuzzy_query, limit=limit)
            
            return [{"id": r["id"], "content": r["content"], "score": r.score, "subject": r.get("subject"), "year": r.get("year"), "tags": r.get("tags"), "options": r.get("options"), "correct_answer": r.get("correct_answer"), "explanation": r.get("explanation")} for r in results]

        except Exception as e:
            print(f"Search error: {e}")
            return []
