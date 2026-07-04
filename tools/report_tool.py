from pathlib import Path

from agent.types import ToolResult
from tools.base_tool import BaseTool


class ReportTool(BaseTool):

    name = "report"
    description = "Creates a markdown report."

    def __init__(self, output_path: Path | str = "report.md"):
        self.output_path = Path(output_path)

    def run(self, tool_input: str) -> ToolResult:
        title, content = self._parse_report_input(tool_input)

        self.output_path.write_text(f"# {title}\n\n{content}", encoding="utf-8")

        return ToolResult(
            success=True,
            content=f"Report created: {self.output_path}",
            data={"file": str(self.output_path)},
        )

    def _parse_report_input(self, tool_input: str) -> tuple[str, str]:
        cleaned_input = tool_input.strip()
        if not cleaned_input:
            return "Agent Report", ""

        title, separator, content = cleaned_input.partition("\n")
        if not separator:
            return title, ""

        return title.strip() or "Agent Report", content.strip()