from llm.ollama_client import generate_response


GRAMMAR_PROMPT = """
You are a grammar and clarity assistant.

Rewrite the user's text with corrected grammar, punctuation, and sentence
structure. Preserve the original meaning and keep the tone professional.
Return only the corrected text without commentary.

Text:
{text}
"""


def improve_grammar(text: str) -> str:
    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError("Text must not be empty.")

    prompt = GRAMMAR_PROMPT.format(text=cleaned_text)
    return generate_response(prompt).strip()
