import json


class Planner:

    def __init__(self, llm):
        self.llm = llm

    def plan(self, user_input: str):

        prompt = f"""
You are a planner for an AI agent.

Choose the best tool.

TOOLS:
- calculator (math operations)
- file (read files)
- report (create markdown report)
- none (just chat)

Return ONLY JSON:

{{
  "tool": "calculator|file|report|none",
  "input": "what to send to tool"
}}

USER INPUT:
{user_input}
"""

        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except:
            return {"tool": "none", "input": user_input}