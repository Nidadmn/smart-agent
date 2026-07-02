from tools.base_tool import BaseTool
import os


class FileTool(BaseTool):

    name = "File"

    description = "Reads a text file."

    def execute(self, file_path):

        if not os.path.exists(file_path):

            return {
                "success": False,
                "error": "File not found."
            }

        try:

            with open(file_path, "r", encoding="utf-8") as f:

                content = f.read()

            return {
                "success": True,
                "content": content
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }