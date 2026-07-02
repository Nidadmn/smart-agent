class Orchestrator:
    def __init__(self, llm, planner, evaluator, tools):
        self.llm = llm
        self.planner = planner
        self.evaluator = evaluator
        self.tools = tools

    def run(self, task: str):

        memory = ""
        max_steps = 5

        for step in range(max_steps):

            # 1. PLAN
            plan = self.planner.plan(task + "\n" + memory)

            if plan is None:
                result = self.llm.generate(task + "\n" + memory)
                return {
                    "final_answer": result,
                    "steps": memory
                }

            tool = self.tools.get(plan["tool"])
            tool_input = plan["input"]

            if tool:
                observation = tool.execute(tool_input)
            else:
                observation = "Tool not found"

            # 2. MEMORY UPDATE
            memory += f"\nStep {step+1}:\nTool: {plan['tool']}\nInput: {tool_input}\nResult: {observation}\n"

            # 3. EVALUATE
            evaluation = self.evaluator.evaluate(task, observation)

            # 4. STOP CONDITION
            if "YES" in evaluation:
                final = self.llm.generate(task + "\n\nResult: " + str(observation))
                return {
                    "final_answer": final,
                    "steps": memory,
                    "evaluation": evaluation
                }

        # fallback
        return {
            "final_answer": "Max steps reached",
            "steps": memory
        }