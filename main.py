from agent.llm import OllamaLLM
from agent.orchestrator import Orchestrator
from agent.planner import Planner
from tools.calculator_tool import CalculatorTool
from tools.file_tool import FileTool
from tools.report_tool import ReportTool


def build_agent() -> Orchestrator:
    llm = OllamaLLM()
    tools = {
        "calculator": CalculatorTool(),
        "file": FileTool(),
        "report": ReportTool(),
    }
    planner = Planner(llm=llm, tool_names=set(tools))
    return Orchestrator(llm=llm, planner=planner, tools=tools)


def main() -> None:
    agent = build_agent()

    print("\nSmart Agent is ready. Type 'exit' or 'quit' to stop.\n")

    while True:
        task = input(">>> ").strip()

        if task.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        if not task:
            continue

        result = agent.run(task)
        print(result.final_answer)
        print("-" * 60)


if __name__ == "__main__":
    main()