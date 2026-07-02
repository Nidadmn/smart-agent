from agent.llm import OllamaLLM
from agent.orchestrator import Orchestrator
from agent.planner import Planner
from agent.evaluator import Evaluator
from tools.calculator_tool import CalculatorTool

# 1. LLM
llm = OllamaLLM(model="qwen2.5:3b")

# 2. Agent parçaları
planner = Planner(llm)
evaluator = Evaluator(llm)

# 3. Tools
tools = {
    "calculator": CalculatorTool()
}

# 4. Orchestrator
agent = Orchestrator(llm, planner, evaluator, tools)

# 5. TEST PROMPT
result = agent.run("2 + 2 hesapla ve sonucu açıkla")

print("\n=== FINAL RESULT ===\n")
print(result)