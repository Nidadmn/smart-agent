class Memory:
    """
    Stores the history of tasks executed by the agent.
    """

    def __init__(self):
        self.history = []

    def add(self, user_input, response):
        self.history.append({
            "input": user_input,
            "response": response
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()