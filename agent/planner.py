import json
import re

from agent.types import Plan


class Planner:

    def __init__(self, llm, tool_names=None):
        self.llm = llm
        self.tool_names = set(tool_names or {"calculator", "file", "report"})

    def plan(self, user_input: str) -> Plan:
        deterministic_plan = self._try_deterministic_plan(user_input)
        if deterministic_plan is not None:
            return deterministic_plan

        prompt = f"""
You are a planner for an AI agent.

Choose the best tool for the user request.

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
        payload = self._parse_json(response)
        if payload is None:
            return Plan(tool="none", tool_input=user_input)

        tool = str(payload.get("tool", "none")).strip().lower()
        tool_input = str(payload.get("input", user_input)).strip()

        if tool == "none":
            return Plan(tool="none", tool_input=user_input)

        if tool not in self.tool_names:
            return Plan(tool="none", tool_input=user_input)

        return Plan(tool=tool, tool_input=tool_input or user_input)

    def _try_deterministic_plan(self, user_input: str) -> Plan | None:
        normalized_input = user_input.strip()
        lower_input = normalized_input.lower()

        if lower_input.startswith("read "):
            return Plan(tool="file", tool_input=normalized_input[5:].strip())

        if lower_input.startswith("report "):
            return Plan(tool="report", tool_input=normalized_input[7:].strip())

        expression = self._extract_math_expression(normalized_input)
        if expression is not None and "calculator" in self.tool_names:
            return Plan(tool="calculator", tool_input=expression)

        return None

    def _extract_math_expression(self, user_input: str) -> str | None:
        if not any(character.isdigit() for character in user_input):
            return None

        matches = re.findall(r"[0-9\s+\-*/().%]+", user_input)
        candidates = [
            match.strip()
            for match in matches
            if any(character.isdigit() for character in match)
        ]

        if not candidates:
            return None

        expression = max(candidates, key=len)
        if not any(operator in expression for operator in "+-*/%"):
            return None

        return expression

    def _parse_json(self, response: str) -> dict | None:
        cleaned_response = response.strip()

        if cleaned_response.startswith("```"):
            cleaned_response = re.sub(r"^```(?:json)?\s*", "", cleaned_response)
            cleaned_response = re.sub(r"\s*```$", "", cleaned_response)

        json_match = re.search(r"\{.*\}", cleaned_response, flags=re.DOTALL)
        if json_match is not None:
            cleaned_response = json_match.group(0)

        try:
            parsed = json.loads(cleaned_response)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        return parsed