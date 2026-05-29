from document_manager.file_registry import find_document_path


def delete_document_file(filename: str) -> dict:
    target_path = find_document_path(filename)
    target_path.unlink()

    return {
        "message": "Document deleted successfully.",
        "filename": filename,
    }
