from typing import override

from .errors import LoxRuntimeError
from .expr_types import Binary, Expr, Grouping, Literal, Unary
from .stmt_types import Expression, Print, Stmt
from .token_type import Token, TokenType


class Interpreter(Expr.Visitor[object], Stmt.Visitor[None]):
    @override
    def visit_literal_expr(self, expr: Literal):
        return expr.value

    @override
    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    @override
    def visit_unary_expr(self, expr: Unary) -> object:
        right = self.evaluate(expr)

        match expr.operator.type:
            case TokenType.BANG:
                return not self.is_truthy(right)
            case TokenType.MINUS:
                return -float(right)  # type: ignore

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
                raise LoxRuntimeError(expr.operator, "Operands must be a number")
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
                return not self.is_equal(left, right)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    @override
    def visit_expression_stmt(self, stmt: Expression):
        self.evaluate(stmt.expression)

    @override
    def visit_print_stmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

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
