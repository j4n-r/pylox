from __future__ import annotations

from enum import Enum
from typing import override

from lox.expr_types import (
    Assign,
    Binary,
    Call,
    Expr,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from lox.interpreter import Interpreter
from lox.stmt_types import (
    Block,
    Expression,
    Function,
    If,
    Print,
    Return,
    Stmt,
    Var,
    While,
)
from lox.token_type import Token


class FunctionType(Enum):
    NONE = "NONE"
    FUNCTION = "FUNCTION"


class Resolver(Expr.Visitor, Stmt.Visitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE

    def resolve(self, input):
        match type(input):
            case list():
                for statement in input:
                    self.resolve(statement)
            case Stmt():
                input.accept(self)
            case Expr():
                input.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if not self.scopes:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def resolve_function(self, function: Function, function_type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = function_type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    # Statement visitors
    @override
    def visit_block_stmt(self, stmt: Block):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    @override
    def visit_var_stmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    @override
    def visit_function_stmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    @override
    def visit_expression_stmt(self, stmt: Expression):
        self.resolve(stmt.expression)

    @override
    def visit_if_stmt(self, stmt: If):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    @override
    def visit_print_stmt(self, stmt: Print):
        self.resolve(stmt.expression)

    @override
    def visit_return_stmt(self, stmt: Return):
        from lox.lox import Lox

        if self.current_function == FunctionType.NONE:
            Lox.error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve(stmt.value)

    @override
    def visit_while_stmt(self, stmt: While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    # Expression visitors
    @override
    def visit_variable_expr(self, expr: Variable):
        from lox.lox import Lox

        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            Lox.error(expr.name, "Can't read local variable in its own initializer")
        self.resolve_local(expr, expr.name)

    @override
    def visit_assign_expr(self, expr: Assign):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    @override
    def visit_binary_expr(self, expr: Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)

    @override
    def visit_call_expr(self, expr: Call):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    @override
    def visit_grouping_expr(self, expr: Grouping):
        self.resolve(expr.expression)

    @override
    def visit_literal_expr(self, expr: Literal):
        # No work to do for literals
        pass

    @override
    def visit_logical_expr(self, expr: Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)

    @override
    def visit_unary_expr(self, expr: Unary):
        self.resolve(expr.right)
