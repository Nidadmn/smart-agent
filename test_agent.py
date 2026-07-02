from agent.orchestrator import Orchestrator
from agent.llm import OllamaLLM
from agent.planner import Planner
from agent.evaluator import Evaluator
from tools.calculator_tool import CalculatorTool
from tools.file_tool import FileTool
from tools.report_tool import ReportTool


def main():

    # LLM
    llm = OllamaLLM()

    # Planner artık LLM kullanıyor (V2 FIX)
    planner = Planner(llm)

    # Evaluator
    evaluator = Evaluator(llm)

    # Tools
    tools = {
        "calculator": CalculatorTool(),
        "file": FileTool(),
        "report": ReportTool()
    }

    # Agent
    agent = Orchestrator(
        llm=llm,
        planner=planner,
        evaluator=evaluator,
        tools=tools
    )

    print("\n🤖 Smart Agent V2 hazır! Çıkmak için 'exit' yaz.\n")

    while True:

        task = input(">>> ").strip()

        if task.lower() in ["exit", "quit"]:
            print("Çıkılıyor...")
            break

        if not task:
            continue

        result = agent.run(task)

        print("\nAGENT SONUÇ:")
        print(result)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()