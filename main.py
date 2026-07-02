from agent.agent import Agent
from workflows.task_workflow import TaskWorkflow

from tools.calculator_tool import CalculatorTool
from tools.file_tool import FileTool
from tools.report_tool import ReportTool


agent = Agent()

agent.register_tool(CalculatorTool())
agent.register_tool(FileTool())
agent.register_tool(ReportTool())

workflow = TaskWorkflow(agent)


while True:

    user = input("\nYou > ")

    if user.lower() == "exit":
        break

    response = workflow.run(user)

    print(response)

    print("\nMemory")

    print(agent.memory.get_history())

    print("-" * 60)