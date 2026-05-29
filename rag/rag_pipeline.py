from retrieval.retriever import retrieve_documents
from llm.ollama_client import generate_response


PROMPT_TEMPLATE = """
You are an offline retrieval-augmented research assistant.

Use only the provided context. If the answer is not supported by the context,
say exactly: "I do not have enough information in the indexed documents."

Context:
{context}

Question:
{question}
"""


def _serialize_sources(docs):
    sources = []
    for doc in docs:
        metadata = dict(doc.metadata)
        metadata["preview"] = doc.page_content[:240]
        sources.append(metadata)
    return sources


def ask_rag(question: str) -> dict:
    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("Question must not be empty.")

    docs = retrieve_documents(cleaned_question)
    if not docs:
        return {
            "answer": "I do not have enough information in the indexed documents.",
            "sources": [],
        }

    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = PROMPT_TEMPLATE.format(context=context, question=cleaned_question)
    response = generate_response(prompt)

    return {
        "answer": response.strip(),
        "sources": _serialize_sources(docs),
    }
