from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from embeddings.embedding_model import embedding_model


BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
INDEX_FILES = ("index.faiss", "index.pkl")


def vector_store_exists() -> bool:
    return all((VECTOR_STORE_DIR / filename).exists() for filename in INDEX_FILES)


def get_vector_store() -> FAISS:
    if not vector_store_exists():
        raise FileNotFoundError(
            "Vector store not found. Run `python ingestion/ingest_pipeline.py` first."
        )

    return FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embedding_model,
        # FAISS metadata is stored via pickle by LangChain. Only load indexes
        # generated locally by this application.
        allow_dangerous_deserialization=True,
    )


def retrieve_documents(query: str, k: int = 5) -> list[Document]:
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("Query must not be empty.")

    retriever = get_vector_store().as_retriever(search_kwargs={"k": k})
    return retriever.invoke(cleaned_query)
