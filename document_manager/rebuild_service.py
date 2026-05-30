import logging
from threading import Lock

from ingestion.ingest_pipeline import build_vector_store
from retrieval.retriever import vector_store_exists

LOGGER = logging.getLogger(__name__)
_rebuild_lock = Lock()
_rebuild_status = {
    "status": "idle",
    "message": "No rebuild has been started yet.",
    "path": None,
}


def _update_rebuild_status(
    *,
    status: str,
    message: str,
    path: str | None = None,
) -> dict:
    _rebuild_status["status"] = status
    _rebuild_status["message"] = message
    _rebuild_status["path"] = path
    return dict(_rebuild_status)


def rebuild_vector_store() -> dict:
    if not _rebuild_lock.acquire(blocking=False):
        return dict(_rebuild_status)

    try:
        _update_rebuild_status(
            status="running",
            message="Vector store rebuild is in progress.",
        )
        vector_store_path = build_vector_store()
        return _update_rebuild_status(
            status="completed",
            message="Vector store rebuilt successfully.",
            path=str(vector_store_path),
        )
    except Exception as exc:
        LOGGER.exception("Vector store rebuild failed")
        return _update_rebuild_status(
            status="failed",
            message=f"Vector store rebuild failed: {exc}",
        )
    finally:
        _rebuild_lock.release()


def queue_rebuild_vector_store() -> dict:
    if _rebuild_lock.locked() or _rebuild_status["status"] == "queued":
        return dict(_rebuild_status)

    return _update_rebuild_status(
        status="queued",
        message="Vector store rebuild has been queued.",
        path=None,
    )


def get_rebuild_status() -> dict:
    return dict(_rebuild_status)


def get_vector_store_status() -> bool:
    return vector_store_exists()
