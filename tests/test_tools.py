import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.calculator_tool import CalculatorTool
from tools.file_tool import FileTool
from tools.report_tool import ReportTool


class CalculatorToolTest(unittest.TestCase):
    def test_evaluates_basic_arithmetic(self):
        result = CalculatorTool().run("2 + 2 * 3")

        self.assertTrue(result.success)
        self.assertEqual(result.content, "8")
        self.assertEqual(result.data["result"], 8)

    def test_rejects_python_code_execution(self):
        result = CalculatorTool().run("__import__('os').system('echo unsafe')")

        self.assertFalse(result.success)
        self.assertIn("Unsupported expression", result.content)


class FileToolTest(unittest.TestCase):
    def test_reads_file_inside_workspace_root(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            notes = root / "notes.txt"
            notes.write_text("hello from file", encoding="utf-8")

            result = FileTool(root_dir=root).run("notes.txt")

        self.assertTrue(result.success)
        self.assertEqual(result.content, "hello from file")

    def test_rejects_paths_outside_workspace_root(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            result = FileTool(root_dir=root).run("../secret.txt")

        self.assertFalse(result.success)
        self.assertIn("outside the workspace", result.content)


class ReportToolTest(unittest.TestCase):
    def test_creates_markdown_report_from_single_input(self):
        with TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "report.md"

            result = ReportTool(output_path=output_path).run(
                "AI Agent Project\nThis is the report body."
            )

            self.assertTrue(result.success)
            self.assertEqual(result.data["file"], str(output_path))
            self.assertEqual(
                output_path.read_text(encoding="utf-8"),
                "# AI Agent Project\n\nThis is the report body.",
            )


if __name__ == "__main__":
    unittest.main()
