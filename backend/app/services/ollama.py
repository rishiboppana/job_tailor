import requests
from ..config import settings

def ollama_generate(prompt: str, model: str = "llama3.1"):
    r = requests.post(
        f"{settings.OLLAMA_URL}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"]
