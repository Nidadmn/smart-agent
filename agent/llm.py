import os

import requests
from dotenv import load_dotenv


DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "qwen3.5:4b"
DEFAULT_OLLAMA_NUM_PREDICT = 160
DEFAULT_OLLAMA_TEMPERATURE = 0.2
DEFAULT_OLLAMA_THINK = False


class OllamaLLM:

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout_seconds: int = 120,
        num_predict: int | None = None,
        temperature: float | None = None,
        think: bool | None = None,
    ):
        load_dotenv(override=False)

        self.model = model or os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
        self.base_url = base_url or os.getenv(
            "OLLAMA_BASE_URL",
            DEFAULT_OLLAMA_BASE_URL
        )
        self.timeout_seconds = timeout_seconds
        self.num_predict = num_predict or int(
            os.getenv("OLLAMA_NUM_PREDICT", DEFAULT_OLLAMA_NUM_PREDICT)
        )
        self.temperature = temperature or float(
            os.getenv("OLLAMA_TEMPERATURE", DEFAULT_OLLAMA_TEMPERATURE)
        )
        self.think = (
            think
            if think is not None
            else self._read_bool_env("OLLAMA_THINK", DEFAULT_OLLAMA_THINK)
        )

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
                "stream": False,
                "think": self.think,
                "options": {
                    "num_predict": self.num_predict,
                    "temperature": self.temperature,
                },
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()

        payload = response.json()
        return str(payload.get("response", "")).strip()

    def _read_bool_env(self, name: str, default: bool) -> bool:
        value = os.getenv(name)
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}