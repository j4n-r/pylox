from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from lox.token_type import Token


@dataclass(frozen=True)
class Expr(ABC):
    @abstractmethod
    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        pass

    class Visitor[R](Protocol):
        def visit_assign_expr(self, expr: Assign) -> R: ...
        def visit_binary_expr(self, expr: Binary) -> R: ...
        def visit_call_expr(self, expr: Call) -> R: ...
        def visit_grouping_expr(self, expr: Grouping) -> R: ...
        def visit_literal_expr(self, expr: Literal) -> R: ...
        def visit_logical_expr(self, expr: Logical) -> R: ...
        def visit_unary_expr(self, expr: Unary) -> R: ...
        def visit_variable_expr(self, expr: Variable) -> R: ...


@dataclass(frozen=True)
class Assign(Expr):
    name: Token
    value: Expr

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_assign_expr(self)


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_binary_expr(self)


@dataclass(frozen=True)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_call_expr(self)


@dataclass(frozen=True)
class Grouping(Expr):
    expression: Expr

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


@dataclass(frozen=True)
class Literal(Expr):
    value: object

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_literal_expr(self)


@dataclass(frozen=True)
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_logical_expr(self)


@dataclass(frozen=True)
class Unary(Expr):
    operator: Token
    right: Expr

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_unary_expr(self)


@dataclass(frozen=True)
class Variable(Expr):
    name: Token

    def accept[R](self, visitor: Expr.Visitor[R]) -> R:
        return visitor.visit_variable_expr(self)
