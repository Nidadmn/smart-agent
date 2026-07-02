import re


class Planner:
    """
    Decides which tool should be used based on the user's request.
    """

    def plan(self, user_input: str):

        user_input = user_input.lower().strip()

        # Basit matematik ifadesi kontrolü
        if re.search(r"[0-9]+\s*[\+\-\*/]\s*[0-9]+", user_input):
            return {
                "tool": "calculator",
                "input": re.search(
                    r"[0-9]+\s*[\+\-\*/]\s*[0-9]+",
                    user_input
                ).group()
            }

        return None