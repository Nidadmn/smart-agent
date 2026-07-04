import unittest

from agent.planner import Planner


class PlannerTest(unittest.TestCase):
    def test_routes_simple_math_without_calling_llm(self):
        planner = Planner(tool_names={"calculator", "file", "report"})

        plan = planner.plan("2 + 2 hesapla")

        self.assertEqual(plan.tool, "calculator")
        self.assertEqual(plan.tool_input, "2 + 2")

    def test_routes_file_read_without_calling_llm(self):
        planner = Planner(tool_names={"calculator", "file", "report"})

        plan = planner.plan("read test.txt")

        self.assertEqual(plan.tool, "file")
        self.assertEqual(plan.tool_input, "test.txt")

    def test_routes_report_command_without_calling_llm(self):
        planner = Planner(tool_names={"calculator", "file", "report"})

        plan = planner.plan("report Title\nBody")

        self.assertEqual(plan.tool, "report")
        self.assertEqual(plan.tool_input, "Title\nBody")

    def test_routes_ambiguous_requests_directly_to_chat(self):
        planner = Planner(tool_names={"calculator"})

        plan = planner.plan("hello")

        self.assertEqual(plan.tool, "none")
        self.assertEqual(plan.tool_input, "hello")


if __name__ == "__main__":
    unittest.main()
