from __future__ import annotations

from lox.expr_types import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from lox.lox import Lox
from lox.stmt_types import Block, Expression, Print, Stmt, Var
from lox.token_type import Token, TokenType


class Parser:
    class ParseError(RuntimeError):
        pass

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def match(self, *types: TokenType) -> bool:
        """Check if the next token is one of the provided ones
        if yes, consumes the token with call to advance()
        """
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def check(self, type):
        """Check if next token is the provided one"""
        if self.is_at_end():
            return False
        return self.peek().type is type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def expression(self) -> Expr:
        return self.assignment()

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except self.ParseError as error:
            self.synchronize()

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LEFT_BRACE) and not self.is_at_end():
            return Block(self.block())
        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return Print(value)

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")

        initializer: Expr | None = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
            self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)  # type: ignore

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression")
        return Expression(expr)

    def block(self):
        statements: list[Stmt] = list()

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())  # type: ignore

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if type(expr) is Variable:
                name = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target")
        return expr

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        Lox.error(token, message)
        return self.ParseError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type is TokenType.SEMICOLON:
                return
            match self.peek().type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return
            self.advance()

    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr: Expr = self.term()
        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr: Expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(
        self,
    ):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.STRING, TokenType.NUMBER):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after Expression.")
            return Grouping(expr)
        raise self.error(self.peek(), "Expect expression")

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.is_at_end():
            statements.append(self.declaration())  # type: ignore

        return statements
