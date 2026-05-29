import os

import ollama


OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
CLIENT = ollama.Client(host=OLLAMA_HOST) if OLLAMA_HOST else ollama.Client()


def generate_response(prompt: str) -> str:
    cleaned_prompt = prompt.strip()
    if not cleaned_prompt:
        raise ValueError("Prompt must not be empty.")

    try:
        response = CLIENT.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": cleaned_prompt}],
        )
    except Exception as exc:
        raise RuntimeError(
            f"Failed to connect to Ollama model `{OLLAMA_MODEL}`. "
            "Ensure Ollama is running and the model is pulled locally."
        ) from exc

    return response["message"]["content"]
