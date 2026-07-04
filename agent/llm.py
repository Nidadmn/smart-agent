import os

import requests
from dotenv import load_dotenv


DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "qwen3.5:4b"


class OllamaLLM:

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout_seconds: int = 120,
    ):
        load_dotenv(override=False)

        self.model = model or os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
        self.base_url = base_url or os.getenv(
            "OLLAMA_BASE_URL",
            DEFAULT_OLLAMA_BASE_URL
        )
        self.timeout_seconds = timeout_seconds

        self.system_prompt = """
You are a helpful AI assistant.
Always respond in Turkish unless user uses English.
Be clear, natural and concise.
Do not say "I’m sorry" unnecessarily.
"""

    def generate(self, prompt: str) -> str:
        full_prompt = f"""
{self.system_prompt}

USER:
{prompt}
"""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()

        payload = response.json()
        return str(payload.get("response", "")).strip()