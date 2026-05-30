from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field

from rag.rag_pipeline import ask_rag
from retrieval.retriever import vector_store_exists

from services.grammar_service import improve_grammar
from services.email_service import generate_email
from services.citation_service import generate_citation
from document_manager.document_service import (
    queue_rebuild,
    save_document,
    rebuild_index,
    list_documents,
    delete_document,
    get_stats
)
from document_manager.rebuild_service import get_rebuild_status


app = FastAPI(
    title="Offline Research Copilot",
    version="1.0.0"
)


# -------------------------
# Request Models
# -------------------------

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User question"
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Input text"
    )


# -------------------------
# Basic Endpoints
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Offline Research Copilot Running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "vector_store_ready": vector_store_exists()
    }


# -------------------------
# RAG Endpoint
# -------------------------

@app.post("/ask")
def ask_question(request: QueryRequest):

    try:

        result = ask_rag(
            request.question
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline failed: {exc}"
        ) from exc


# -------------------------
# Grammar Assistant
# -------------------------

@app.post("/grammar")
def grammar(request: TextRequest):

    try:

        result = improve_grammar(
            request.text
        )

        return {
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Grammar service failed: {exc}"
        ) from exc


# -------------------------
# Email Generator
# -------------------------

@app.post("/email")
def email(request: TextRequest):

    try:

        result = generate_email(
            request.text
        )

        return {
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Email service failed: {exc}"
        ) from exc


# -------------------------
# Citation Generator
# -------------------------

@app.post("/citation")
def citation(request: TextRequest):

    try:

        result = generate_citation(
            request.text
        )

        return {
            "result": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Citation service failed: {exc}"
        ) from exc
    
@app.post("/upload")
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    try:
        path = save_document(file)
        rebuild_state = queue_rebuild()
        if rebuild_state["status"] == "queued":
            background_tasks.add_task(rebuild_index)

        return {
            "message": "Uploaded",
            "path": path,
            "rebuild_status": rebuild_state,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {exc}",
        ) from exc


@app.get("/documents")
def documents():

    return list_documents()


@app.delete("/documents/{filename}")
def remove_document(
    filename: str
):

    return delete_document(
        filename
    )


@app.post("/rebuild")
def rebuild(background_tasks: BackgroundTasks):
    rebuild_state = queue_rebuild()
    if rebuild_state["status"] == "queued":
        background_tasks.add_task(rebuild_index)
    return rebuild_state


@app.get("/rebuild-status")
def rebuild_status():
    return get_rebuild_status()


@app.get("/stats")
def stats():

    return get_stats()
