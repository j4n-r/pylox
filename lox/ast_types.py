from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Protocol

from .token import Token


@dataclass
class Expr:
    pass

    class Visitor(Protocol):
        def visit_binary_expr(self, expr: Binary) -> object: ...
        def visit_grouping_expr(self, expr: Grouping) -> object: ...
        def visit_literal_expr(self, expr: Literal) -> object: ...
        def visit_unary_expr(self, expr: Unary) -> object: ...


@dataclass
class Binary(Expr):
    left: Final[Expr]
    operator: Final[Token]
    right: Final[Expr]

    def accept(self, visitor: Expr.Visitor) -> object:
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Final[Expr]

    def accept(self, visitor: Expr.Visitor) -> object:
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: Final[object]

    def accept(self, visitor: Expr.Visitor) -> object:
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Final[Token]
    right: Final[Expr]

    def accept(self, visitor: Expr.Visitor) -> object:
        return visitor.visit_unary_expr(self)
