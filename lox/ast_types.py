from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, Protocol

from token_type import Token


@dataclass
class Expr(ABC):
    pass

    @abstractmethod
    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        pass

    class Visitor[R](Protocol):
        def visit_binary_expr(self, expr: Binary) -> R: ...
        def visit_grouping_expr(self, expr: Grouping) -> R: ...
        def visit_literal_expr(self, expr: Literal) -> R: ...
        def visit_unary_expr(self, expr: Unary) -> R: ...


@dataclass
class Binary(Expr):
    left: Final[Expr]
    operator: Final[Token]
    right: Final[Expr]

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Final[Expr]

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: Final[object]

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Final[Token]
    right: Final[Expr]

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_unary_expr(self)
