
from pathlib import Path
import re

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
POLICY_DIR = PROJECT_ROOT / "data" / "policies"

class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

def tokenize(text: str) -> set[str]:
    return set(re.findall(r"\b[a-zA-Z0-9]+\b", text.lower()))

def retrieve_documents(question: str, top_k: int = 3):
    question_terms = tokenize(question)
    results = []

    if not POLICY_DIR.exists():
        return results

    for path in POLICY_DIR.glob("*.txt"):
        content = path.read_text(encoding="utf-8")
        paragraphs = [
            p.strip() for p in re.split(r"\n\s*\n", content)
            if p.strip()
        ]

        for paragraph in paragraphs:
            paragraph_terms = tokenize(paragraph)
            overlap = question_terms & paragraph_terms

            if overlap:
                results.append({
                    "source": path.name,
                    "text": paragraph,
                    "matched_terms": sorted(overlap),
                    "score": round(
                        len(overlap) / max(len(question_terms), 1), 3
                    ),
                })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]

@router.get("/")
def rag_home():
    return {
        "module": "Policy Retrieval API",
        "retrieval_method": "Keyword overlap",
        "policy_directory": str(POLICY_DIR),
        "note": "Starter retrieval module; not yet embedding-based RAG."
    }

@router.post("/ask")
def ask_policy(request: QuestionRequest):
    documents = retrieve_documents(request.question)

    if not documents:
        return {
            "question": request.question,
            "answer": (
                "I could not find a matching passage in the local "
                "policy documents. Please consult the approved policy."
            ),
            "sources": [],
            "retrieval_method": "keyword"
        }

    excerpts = [
        {
            "source": doc["source"],
            "text": doc["text"],
            "score": doc["score"]
        }
        for doc in documents
    ]

    return {
        "question": request.question,
        "answer": (
            "Relevant policy excerpts were retrieved. Review the "
            "sources below; this endpoint does not generate an "
            "AI-written answer."
        ),
        "sources": excerpts,
        "retrieval_method": "keyword"
    }