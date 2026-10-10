
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai

# Load E:\Banking_Data_Analysis\backend\.env
load_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".env",
    )
)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

app = FastAPI(
    title="Banking Data Analysis API",
    description="API for banking analytics and RAG integration",
    version="1.0.0",
)

# React frontend CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class RAGQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


@app.get("/")
def home():
    return {
        "message": "Banking Data Analysis API is running",
        "status": "success",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "banking-backend",
    }


def ask_gemini(question: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing from backend/.env",
        )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=(
                "You are a banking analytics assistant. "
                "Answer clearly and never invent financial figures. "
                "You do not have access to the banking database yet. "
                "If a question requires actual transaction, loan, "
                "customer, or fraud data, explain that the database "
                "must be connected before you can provide the result.\n\n"
                f"Question: {question}"
            ),
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response.",
            )

        return response.text

    except HTTPException:
        raise
    except Exception as exc:
        print(f"Gemini error: {exc}")
        raise HTTPException(
            status_code=502,
            detail=(
                "Gemini request failed. Check the backend terminal "
                "for the actual error and verify the model name and API key."
            ),
        ) from exc


# Endpoint used by AIChat.jsx
@app.post("/api/rag/ask")
def ask_rag(request: RAGQuestion):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question.",
        )

    return {
        "answer": ask_gemini(question),
        "sources": [],
    }


# Preserve the original chat endpoint
@app.post("/api/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question.",
        )

    return {
        "answer": ask_gemini(message),
        "sources": [],
    }
