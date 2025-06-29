from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, Protocol

from lox.expr_types import Expr
from lox.token_type import Token


@dataclass
class Stmt(ABC):
    pass

    @abstractmethod
    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        pass

    class Visitor[R](Protocol):
        def visit_expression_stmt(self, stmt: Expression) -> R: ...
        def visit_print_stmt(self, stmt: Print) -> R: ...
        def visit_var_stmt(self, stmt: Var) -> R: ...


@dataclass
class Expression(Stmt):
    expression: Final[Expr]

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expression: Final[Expr]

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_print_stmt(self)


@dataclass
class Var(Stmt):
    name: Final[Token]
    initializer: Final[Expr | None]

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_var_stmt(self)
