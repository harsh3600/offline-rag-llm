from pathlib import Path

from fastapi import UploadFile

from document_manager.delete_service import delete_document_file
from document_manager.file_registry import iter_document_paths
from document_manager.rebuild_service import (
    get_vector_store_status,
    rebuild_vector_store,
)
from document_manager.upload_service import save_uploaded_file


def _serialize_document(file_path: Path) -> dict:
    return {
        "filename": file_path.name,
        "path": str(file_path),
        "size_bytes": file_path.stat().st_size,
        "extension": file_path.suffix.lower(),
    }


def save_document(file: UploadFile) -> str:
    return save_uploaded_file(file)


def rebuild_index() -> dict:
    return rebuild_vector_store()


def list_documents() -> list[dict]:
    return [_serialize_document(file_path) for file_path in iter_document_paths()]


def delete_document(filename: str) -> dict:
    return delete_document_file(filename)


def get_stats() -> dict:
    documents = iter_document_paths()
    total_size = sum(file_path.stat().st_size for file_path in documents)

    return {
        "documents": len(documents),
        "total_size_bytes": total_size,
        "vector_store_ready": get_vector_store_status(),
    }
