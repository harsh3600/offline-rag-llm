from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag.rag_pipeline import ask_rag
from retrieval.retriever import vector_store_exists


app = FastAPI(title="Offline RAG API", version="1.0.0")


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")


@app.get("/")
def home():
    return {"message": "Offline RAG API running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "vector_store_ready": vector_store_exists(),
    }


@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        return ask_rag(request.question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline failed: {exc}",
        ) from exc
