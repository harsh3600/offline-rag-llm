from llm.ollama_client import generate_response


EMAIL_PROMPT = """
You are an email writing assistant.

Write a clear, professional email based on the user's instruction.
Include a subject line at the top. Return only the email content.

Instruction:
{text}
"""


def generate_email(text: str) -> str:
    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError("Text must not be empty.")

    prompt = EMAIL_PROMPT.format(text=cleaned_text)
    return generate_response(prompt).strip()
