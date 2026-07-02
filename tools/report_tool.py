from tools.base_tool import BaseTool

class ReportTool(BaseTool):

    name = "report"
    description = "Creates a markdown report."

    def run(self, title, content):
        filename = "report.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(content)

        return {
            "success": True,
            "file": filename
        }