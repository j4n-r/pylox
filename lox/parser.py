from __future__ import annotations

from typing import Final

from ast_types import Binary, Expr
from token_type import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: Final[list[Token]] = tokens
        self.current: int = 0

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def check(self, type):
        if self.is_at_end():
            return False
        return self.peek().type is type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self):
        return self.tokens[self.current + 1]

    def previous(self):
        return self.tokens[self.current - 1]

    def expression(self) -> Expr:
        return self.equality()

    def is_at_end(self):
        return self.peek() == TokenType.EOF

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
        pass
