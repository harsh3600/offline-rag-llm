from pathlib import Path

from fastapi import UploadFile

from document_manager.file_registry import (
    ensure_document_directories,
    get_target_directory,
)


def save_uploaded_file(file: UploadFile) -> str:
    filename = Path(file.filename or "").name
    if not filename:
        raise ValueError("Uploaded file must have a filename.")

    ensure_document_directories()
    target_directory = get_target_directory(filename)
    target_path = target_directory / filename

    contents = file.file.read()
    if not contents:
        raise ValueError("Uploaded file is empty.")

    target_path.write_bytes(contents)
    return str(target_path)
