from ingestion.ingest_pipeline import build_vector_store
from retrieval.retriever import vector_store_exists


def rebuild_vector_store() -> dict:
    vector_store_path = build_vector_store()
    return {
        "message": "Vector store rebuilt successfully.",
        "path": str(vector_store_path),
    }


def get_vector_store_status() -> bool:
    return vector_store_exists()
