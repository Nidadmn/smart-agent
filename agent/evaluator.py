class Evaluator:
    """
    Evaluates whether a tool execution was successful.
    """

    def evaluate(self, result):

        if not isinstance(result, dict):
            return False

        return result.get("success", False)