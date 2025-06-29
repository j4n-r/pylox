from __future__ import annotations

from typing import override

from lox.expr_types import Binary, Expr, Grouping, Literal, Unary


class AstPrinter(Expr.Visitor):
    def print(self, expr: Expr) -> object:
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        str = f"({name}"
        for expr in exprs:
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
