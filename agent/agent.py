from agent.planner import Planner
from memory.memory import Memory


class Agent:

    def __init__(self):

        self.tools = {}

        self.planner = Planner()

        self.memory = Memory()

    def register_tool(self, tool):

        self.tools[tool.name.lower()] = tool

    def process(self, user_input):

        plan = self.planner.plan(user_input)

        if plan is None:
            return {
                "success": False,
                "error": "No suitable tool found."
            }

        tool = self.tools.get(plan["tool"])

        if tool is None:
            return {
                "success": False,
                "error": "Tool not registered."
            }

        tool_input = plan["input"]

        if isinstance(tool_input, tuple):
            result = tool.execute(*tool_input)
        else:
            result = tool.execute(tool_input)

        self.memory.add(user_input, result)

        return result