from __future__ import annotations

from typing import override

from ast_types import Binary, Expr, Grouping, Literal, Unary
from token_type import Token, TokenType


class AstPrinter(Expr.Visitor):
    def print(self, expr: Expr) -> object:
        return expr.accept(self)

    def parenthesize(self, name: str, *args: Expr) -> str:
        str = f"({name}"
        for expr in args:
            str += f" {expr.accept(self)}"
        str += ")"
        return str

    @override
    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @override
    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    @override
    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    @override
    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)


expression = Binary(
    Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(Literal(45.67)),
)
print(AstPrinter().print(expression))
