class Evaluator:
    def __init__(self, llm):
        self.llm = llm

    def evaluate(self, task, result):
        prompt = f"""
Task: {task}
Result: {result}

Is this correct? Answer YES or NO and explain briefly.
"""
        return self.llm.generate(prompt)