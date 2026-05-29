from llm.ollama_client import generate_response


CITATION_PROMPT = """
You are a citation formatting assistant.

Generate a clean academic citation from the user's details. If the format is
not specified, use APA style. Return only the citation.

Details:
{text}
"""


def generate_citation(text: str) -> str:
    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError("Text must not be empty.")

    prompt = CITATION_PROMPT.format(text=cleaned_text)
    return generate_response(prompt).strip()
