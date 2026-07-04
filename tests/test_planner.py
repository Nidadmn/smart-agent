import unittest

from agent.planner import Planner


class FakeLLM:
    def __init__(self, response):
        self.response = response
        self.prompts = []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return self.response


class PlannerTest(unittest.TestCase):
    def test_routes_simple_math_without_calling_llm(self):
        llm = FakeLLM('{"tool": "none", "input": "unused"}')
        planner = Planner(llm, tool_names={"calculator", "file", "report"})

        plan = planner.plan("2 + 2 hesapla")

        self.assertEqual(plan.tool, "calculator")
        self.assertEqual(plan.tool_input, "2 + 2")
        self.assertEqual(llm.prompts, [])

    def test_routes_file_read_without_calling_llm(self):
        llm = FakeLLM('{"tool": "none", "input": "unused"}')
        planner = Planner(llm, tool_names={"calculator", "file", "report"})

        plan = planner.plan("read test.txt")

        self.assertEqual(plan.tool, "file")
        self.assertEqual(plan.tool_input, "test.txt")
        self.assertEqual(llm.prompts, [])

    def test_parses_json_from_llm_for_ambiguous_requests(self):
        llm = FakeLLM('```json\n{"tool": "report", "input": "Title\\nBody"}\n```')
        planner = Planner(llm, tool_names={"calculator", "file", "report"})

        plan = planner.plan("create a report")

        self.assertEqual(plan.tool, "report")
        self.assertEqual(plan.tool_input, "Title\nBody")

    def test_falls_back_to_chat_when_llm_returns_invalid_json(self):
        planner = Planner(FakeLLM("not json"), tool_names={"calculator"})

        plan = planner.plan("hello")

        self.assertEqual(plan.tool, "none")
        self.assertEqual(plan.tool_input, "hello")


if __name__ == "__main__":
    unittest.main()
