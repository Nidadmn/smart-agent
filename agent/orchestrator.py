from agent.types import AgentResult, HistoryEntry, ToolResult


class Orchestrator:
    def __init__(self, llm, planner, tools, history=None):
        self.llm = llm
        self.planner = planner
        self.tools = tools
        self.history = history or []

    def run(self, task: str) -> AgentResult:
        plan = self.planner.plan(task)

        if plan.tool == "none":
            final_answer = self.llm.generate(task)
            result = AgentResult(final_answer=final_answer, plan=plan)
            self._add_history(task, final_answer)
            return result

        tool = self.tools.get(plan.tool)
        if tool is None:
            tool_result = ToolResult(
                success=False,
                content=f"Tool is not registered: {plan.tool}",
            )
            result = AgentResult(
                final_answer=tool_result.content,
                plan=plan,
                tool_result=tool_result,
            )
            self._add_history(task, tool_result.content)
            return result

        tool_result = tool.run(plan.tool_input)
        final_answer = tool_result.content
        result = AgentResult(
            final_answer=final_answer,
            plan=plan,
            tool_result=tool_result,
        )
        self._add_history(task, final_answer)
        return result

    def _add_history(self, user_input: str, response: str) -> None:
        self.history.append(HistoryEntry(user_input=user_input, response=response))