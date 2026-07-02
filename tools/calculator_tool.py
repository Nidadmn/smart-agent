from tools.base_tool import BaseTool

class CalculatorTool(BaseTool):

    name = "calculator"
    description = "Performs basic mathematical calculations."

    def run(self, expression: str):
        try:
            result = eval(expression)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }