import logging
from pathlib import Path

from langchain.vectorstores import FAISS
from langchain.schema import Document

from embeddings.embedding_model import embedding_model
from ingestion.chunking import split_documents
from ingestion.doc_loader import load_docx
from ingestion.excel_loader import load_excel
from ingestion.pdf_loader import load_pdf


LOGGER = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
DOC_DIR = DATA_DIR / "docs"
EXCEL_DIR = DATA_DIR / "excels"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def ensure_data_directories() -> None:
    for directory in (PDF_DIR, DOC_DIR, EXCEL_DIR, VECTOR_STORE_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def _load_files_from_directory(
    directory: Path,
    pattern: str,
    loader_func,
) -> list[Document]:
    documents: list[Document] = []
    for file_path in sorted(directory.glob(pattern)):
        LOGGER.info("Loading %s", file_path)
        docs = loader_func(str(file_path))
        documents.extend(docs)
    return documents


def load_all_documents() -> list[Document]:
    ensure_data_directories()

    documents: list[Document] = []
    documents.extend(_load_files_from_directory(PDF_DIR, "*.pdf", load_pdf))
    documents.extend(_load_files_from_directory(DOC_DIR, "*.docx", load_docx))
    documents.extend(_load_files_from_directory(EXCEL_DIR, "*.xlsx", load_excel))
    documents.extend(_load_files_from_directory(EXCEL_DIR, "*.xls", load_excel))

    if not documents:
        raise ValueError(
            "No source documents were found. Add files under "
            f"{PDF_DIR}, {DOC_DIR}, or {EXCEL_DIR} and rerun ingestion."
        )

    LOGGER.info("Loaded %s raw documents", len(documents))
    return documents


def build_vector_store() -> Path:
    documents = load_all_documents()
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("Chunking produced no output documents.")

    LOGGER.info("Created %s chunks", len(chunks))

    vector_db = FAISS.from_documents(chunks, embedding_model)
    vector_db.save_local(str(VECTOR_STORE_DIR))

    LOGGER.info("Vector store saved to %s", VECTOR_STORE_DIR)
    return VECTOR_STORE_DIR


def main() -> None:
    configure_logging()
    build_vector_store()
    print(f"Vector database created successfully at {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    main()
