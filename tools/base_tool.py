from abc import ABC, abstractmethod

from agent.types import ToolResult


class BaseTool(ABC):
    """Base interface for all agent tools."""

    name = "Base Tool"
    description = "Abstract Tool"

    @abstractmethod
    def run(self, tool_input: str) -> ToolResult:
        """Execute the tool with a single string input."""
        pass