import os
import unittest
from unittest.mock import patch

from agent.llm import OllamaLLM


class OllamaLLMConfigTest(unittest.TestCase):
    def test_uses_modern_documented_defaults_when_env_is_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            llm = OllamaLLM()

        self.assertEqual(llm.model, "qwen3.5:4b")
        self.assertEqual(llm.base_url, "http://localhost:11434")
        self.assertEqual(llm.num_predict, 160)
        self.assertEqual(llm.temperature, 0.2)
        self.assertFalse(llm.think)

    def test_environment_variables_override_default_ollama_config(self):
        with patch.dict(
            os.environ,
            {
                "OLLAMA_MODEL": "ornith:9b",
                "OLLAMA_BASE_URL": "http://ollama:11434",
                "OLLAMA_NUM_PREDICT": "64",
                "OLLAMA_TEMPERATURE": "0.1",
                "OLLAMA_THINK": "true",
            },
            clear=True,
        ):
            llm = OllamaLLM()

        self.assertEqual(llm.model, "ornith:9b")
        self.assertEqual(llm.base_url, "http://ollama:11434")
        self.assertEqual(llm.num_predict, 64)
        self.assertEqual(llm.temperature, 0.1)
        self.assertTrue(llm.think)


if __name__ == "__main__":
    unittest.main()
