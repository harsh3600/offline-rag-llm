# Offline RAG LLM

Local retrieval-augmented generation stack for PC deployment using:

- local document ingestion for PDF, DOCX, XLS/XLSX
- FAISS vector search
- Hugging Face embeddings
- Ollama-hosted local LLM
- FastAPI backend
- Streamlit desktop-style UI

## Architecture

```text
Documents -> Loaders -> Chunking -> Embeddings -> FAISS -> Retriever -> Ollama -> Answer
```

## Repository Layout

```text
offline-rag-llm/
|-- api/
|-- data/
|   |-- pdfs/
|   |-- docs/
|   `-- excels/
|-- embeddings/
|-- ingestion/
|-- llm/
|-- rag/
|-- retrieval/
|-- ui/
|-- vector_store/
|-- requirements.txt
`-- Readme.md
```

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install and prepare Ollama

Install Ollama from `https://ollama.com`.

Pull the local model:

```bash
ollama pull qwen2.5:7b
```

Optional environment variables:

```bash
set OLLAMA_MODEL=qwen2.5:7b
set OLLAMA_HOST=http://127.0.0.1:11434
```

## Data Preparation

Place documents in:

- `data/pdfs/`
- `data/docs/`
- `data/excels/`

Excel ingestion is row-level with sheet metadata, so retrieval can cite a specific sheet and row.

## Build the Vector Store

```bash
python ingestion/ingest_pipeline.py
```

The ingestion pipeline:

- creates missing `data/` and `vector_store/` directories
- loads all supported files
- chunks documents
- builds a FAISS index
- saves the index under `vector_store/`

If no documents are found, the pipeline fails with a clear message instead of crashing on `os.listdir`.

## Run the Backend

```bash
uvicorn api.main:app --reload
```

Useful endpoints:

- `GET /` basic status
- `GET /health` API status plus vector store readiness
- `POST /ask` RAG question answering

Example request:

```json
{
  "question": "What does the contract say about termination notice?"
}
```

## Run the UI

```bash
streamlit run ui/app.py
```

The UI checks API connectivity and whether the vector store exists before sending queries.

## Current Behavior

- empty question returns `400`
- missing vector store returns `503`
- Ollama connectivity failures are surfaced as API errors
- unsupported answers are instructed to abstain when the indexed context is insufficient

## Recommended Next Upgrades

For a serious offline PC product, the strongest next steps are:

1. Add document-level and chunk-level metadata filters.
2. Add OCR for scanned PDFs and images.
3. Add reranking with a local cross-encoder.
4. Add persistent app configuration instead of environment-only settings.
5. Add packaging for Windows desktop deployment.
6. Add automated tests for ingestion, retrieval, and API error paths.
