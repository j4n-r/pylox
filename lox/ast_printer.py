from __future__ import annotations

from typing import override

from ast_types import Binary, Expr


class AstPrinter(Expr.Visitor):
    def print(self, expr: Expr) -> object:
        return expr.accept(self)

    def parenthsize(self, name: str, *args: Expr):
        str = f"({name}"
        for expr in args:
            str += f" {expr.accept(self)}"

    @override
    def visit_binary_expr(self, expr: Binary) -> object:
        return parenthesize(expr.operator.lexeme, expr.left, expr.right)
