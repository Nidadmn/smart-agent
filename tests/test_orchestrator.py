import unittest

from agent.orchestrator import Orchestrator
from agent.types import Plan, ToolResult


class FakeLLM:
    def __init__(self, response="chat response"):
        self.response = response
        self.prompts = []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return self.response


class FakePlanner:
    def __init__(self, plan):
        self.next_plan = plan

    def plan(self, task):
        return self.next_plan


class FakeTool:
    name = "calculator"
    description = "Fake calculator."

    def __init__(self):
        self.inputs = []

    def run(self, tool_input):
        self.inputs.append(tool_input)
        return ToolResult(success=True, content="4", data={"result": 4})


class OrchestratorTest(unittest.TestCase):
    def test_runs_selected_tool_and_returns_tool_result(self):
        llm = FakeLLM()
        tool = FakeTool()
        agent = Orchestrator(
            llm=llm,
            planner=FakePlanner(Plan(tool="calculator", tool_input="2 + 2")),
            tools={"calculator": tool},
        )

        result = agent.run("2 + 2 hesapla")

        self.assertEqual(result.final_answer, "4")
        self.assertEqual(tool.inputs, ["2 + 2"])
        self.assertEqual(llm.prompts, [])
        self.assertEqual(len(agent.history), 1)
        self.assertEqual(agent.history[0].user_input, "2 + 2 hesapla")
        self.assertEqual(agent.history[0].response, "4")

    def test_uses_llm_directly_for_chat_plan(self):
        llm = FakeLLM(response="Merhaba.")
        agent = Orchestrator(
            llm=llm,
            planner=FakePlanner(Plan(tool="none", tool_input="hello")),
            tools={},
        )

        result = agent.run("hello")

        self.assertEqual(result.final_answer, "Merhaba.")
        self.assertEqual(llm.prompts, ["hello"])


if __name__ == "__main__":
    unittest.main()
