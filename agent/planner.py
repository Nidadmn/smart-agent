import re

from agent.types import Plan


class Planner:

    def __init__(self, tool_names=None):
        self.tool_names = set(tool_names or {"calculator", "file", "report"})

    def plan(self, user_input: str) -> Plan:
        deterministic_plan = self._try_deterministic_plan(user_input)
        if deterministic_plan is not None:
            return deterministic_plan

        return Plan(tool="none", tool_input=user_input)

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