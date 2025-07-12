from __future__ import annotations

import time
from typing import override

from lox.environment import Environment
from lox.errors import LoxRuntimeError
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
from lox.lox_callable import LoxCallable
from lox.lox_function import LoxFunction
from lox.lox_return import LoxReturn
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
from lox.token_type import Token, TokenType


class Interpreter(Expr.Visitor[object], Stmt.Visitor[None]):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

        class ClockCallable(LoxCallable):
            def arity(self) -> int:
                return 0

            @override
            def call(self, interpreter: Interpreter, arguments: list[object]) -> object:
                return time.time()

            def __str__(self) -> str:
                return "<native fn>"

        self.globals.define("clock", ClockCallable())

    @override
    def visit_literal_expr(self, expr: Literal):
        return expr.value

    @override
    def visit_logical_expr(self, expr: Logical):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)

    @override
    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    @override
    def visit_unary_expr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG:
                return not self.is_truthy(right)
            case TokenType.MINUS:
                return -float(right)  # type: ignore

    @override
    def visit_variable_expr(self, expr: Variable):
        return self.environment.get(expr.name)

    @override
    def visit_binary_expr(self, expr: Binary) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return float(left) - float(right)  # type: ignore
            case TokenType.PLUS:
                if isinstance(left, (float, int)) and isinstance(right, (float, int)):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise LoxRuntimeError(expr.operator, "Operands must be numbers")
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)  # type: ignore
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)  # type: ignore
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)  # type:ignore
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)  # type:ignore
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)  # type: ignore
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)  # type: ignore
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

    @override
    def visit_call_expr(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments: list[object] = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")

        function: LoxCallable = callee
        if len(arguments) != function.arity():
            raise LoxRuntimeError(
                expr.paren,
                f"Expected {function.arity()} arguments but got {len(arguments)}",
            )
        return function.call(self, arguments)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    @override
    def visit_block_stmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    @override
    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)

    @override
    def visit_function_stmt(self, stmt: Function):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    @override
    def visit_if_stmt(self, stmt: If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    @override
    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    @override
    def visit_return_stmt(self, stmt: Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise LoxReturn(value)

    @override
    def visit_var_stmt(self, stmt: Var):
        value: object | None = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    @override
    def visit_while_stmt(self, stmt: While):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    @override
    def visit_assign_expr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def is_truthy(self, object: object):
        if object is None or object is False:
            return False
        return True

    def is_equal(self, a: object, b: object):
        return a is b or a == b

    def check_number_operand(self, operator: Token, operand: object):
        if isinstance(operand, (float, int)):
            return
        raise LoxRuntimeError(operator, "Operand must be a number")

    def check_number_operands(self, operator: Token, left: object, right: object):
        if isinstance(left, (float, int)) and isinstance(right, (float, int)):
            return
        raise LoxRuntimeError(operator, "Operands must be a number")

    def stringify(self, object: object) -> str:
        if object is None:
            return "nil"
        if isinstance(object, float) and object.is_integer():
            return str(int(object))
        return str(object)

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as error:
            from lox.lox import Lox

            Lox.runtime_error(error)
