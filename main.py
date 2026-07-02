from agent.agent import Agent
from tools.calculator_tool import CalculatorTool


agent = Agent()

agent.register_tool(CalculatorTool())

while True:

    user = input("You > ")

    if user.lower() == "exit":
        break

    response = agent.process(user)

    print(response)