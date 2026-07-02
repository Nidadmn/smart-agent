import requests


class OllamaLLM:

    def __init__(self, model="qwen2.5:3b"):
        self.model = model
        self.base_url = "http://localhost:11434"

        # 🔥 KRİTİK FIX: davranış standardı
        self.system_prompt = """
You are a helpful AI assistant.
Always respond in Turkish unless user uses English.
Be clear, natural and concise.
Do not say "I’m sorry" unnecessarily.
"""

    def generate(self, prompt):

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
            }
        )

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.text}"