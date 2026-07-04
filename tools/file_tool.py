from pathlib import Path

from agent.types import ToolResult
from tools.base_tool import BaseTool


class FileTool(BaseTool):

    name = "file"
    description = "Reads a text file."

    def __init__(self, root_dir: Path | str | None = None):
        self.root_dir = Path(root_dir or ".").resolve()

    def run(self, tool_input: str) -> ToolResult:
        try:
            file_path = self._resolve_path(tool_input)
            content = file_path.read_text(encoding="utf-8")
        except (FileNotFoundError, IsADirectoryError, ValueError) as error:
            return ToolResult(success=False, content=str(error))
        except OSError as error:
            return ToolResult(success=False, content=f"Could not read file: {error}")

        return ToolResult(success=True, content=content, data={"file": str(file_path)})

    def _resolve_path(self, tool_input: str) -> Path:
        requested_path = (self.root_dir / tool_input.strip()).resolve()

        if not requested_path.is_relative_to(self.root_dir):
            raise ValueError("File path is outside the workspace.")

        if not requested_path.exists():
            raise FileNotFoundError("File not found.")

        if requested_path.is_dir():
            raise IsADirectoryError("Path is a directory, not a file.")

        return requested_path