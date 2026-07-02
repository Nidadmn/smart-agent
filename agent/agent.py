from agent.planner import Planner


class Agent:

    def __init__(self):

        self.tools = {}

        self.planner = Planner()

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

        return tool.execute(plan["input"])