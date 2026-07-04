import ast
import operator

from agent.types import ToolResult
from tools.base_tool import BaseTool


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorTool(BaseTool):

    name = "calculator"
    description = "Performs basic mathematical calculations."

    def run(self, tool_input: str) -> ToolResult:
        try:
            result = self._evaluate(tool_input)
        except (SyntaxError, ValueError, ZeroDivisionError) as error:
            return ToolResult(success=False, content=str(error))

        return ToolResult(
            success=True,
            content=self._format_number(result),
            data={"result": result},
        )

    def _evaluate(self, expression: str) -> int | float:
        if not expression.strip():
            raise ValueError("Expression cannot be empty.")

        parsed = ast.parse(expression, mode="eval")
        return self._evaluate_node(parsed.body)

    def _evaluate_node(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)
            if operator_type not in _BINARY_OPERATORS:
                raise ValueError("Unsupported expression.")
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            return _BINARY_OPERATORS[operator_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)
            if operator_type not in _UNARY_OPERATORS:
                raise ValueError("Unsupported expression.")
            operand = self._evaluate_node(node.operand)
            return _UNARY_OPERATORS[operator_type](operand)

        raise ValueError("Unsupported expression.")

    def _format_number(self, value: int | float) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)