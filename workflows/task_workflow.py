from agent.evaluator import Evaluator


class TaskWorkflow:

    def __init__(self, agent):

        self.agent = agent

        self.evaluator = Evaluator()

    def run(self, user_input):

        result = self.agent.process(user_input)

        success = self.evaluator.evaluate(result)

        return {
            "success": success,
            "result": result
        }