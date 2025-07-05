from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from lox.token_type import Token
from lox.expr_types import Expr


@dataclass
class Stmt(ABC):
    pass
    
    @abstractmethod
    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        pass

    class Visitor[R](Protocol):
        def visit_block_stmt(self, stmt: Block) -> R: ...
        def visit_expression_stmt(self, stmt: Expression) -> R: ...
        def visit_function_stmt(self, stmt: Function) -> R: ...
        def visit_print_stmt(self, stmt: Print) -> R: ...
        def visit_if_stmt(self, stmt: If) -> R: ...
        def visit_var_stmt(self, stmt: Var) -> R: ...
        def visit_while_stmt(self, stmt: While) -> R: ...

@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_block_stmt(self)

@dataclass
class Expression(Stmt):
    expression: Expr

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_expression_stmt(self)

@dataclass
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_function_stmt(self)

@dataclass
class Print(Stmt):
    expression: Expr

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_print_stmt(self)

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_if_stmt(self)

@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_var_stmt(self)

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

    def accept[R](self, visitor: Stmt.Visitor[R]) -> R:
        return visitor.visit_while_stmt(self)

