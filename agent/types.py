from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Plan:
    tool: str
    tool_input: str


@dataclass(frozen=True)
class ToolResult:
    success: bool
    content: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentResult:
    final_answer: str
    plan: Plan
    tool_result: ToolResult | None = None


@dataclass(frozen=True)
class HistoryEntry:
    user_input: str
    response: str
