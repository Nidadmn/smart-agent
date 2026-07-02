import re


class Planner:
    """
    Decides which tool should be used based on the user's request.
    """

    def plan(self, user_input: str):

        text = user_input.lower().strip()

        # -------------------------
        # Calculator
        # -------------------------

        expression = re.search(
            r"[0-9]+\s*[\+\-\*/]\s*[0-9]+",
            text
        )

        if expression:

            return {
                "tool": "calculator",
                "input": expression.group()
            }

        # -------------------------
        # File Reader
        # -------------------------

        if text.startswith("read "):

            filename = user_input[5:].strip()

            return {
                "tool": "file",
                "input": filename
            }

        # -------------------------
        # Report
        # -------------------------

        if text.startswith("report "):

            content = user_input[7:].strip()

            return {
                "tool": "report",
                "input": (
                    "Agent Report",
                    content
                )
            }

        return None