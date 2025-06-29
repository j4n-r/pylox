from __future__ import annotations

from lox.errors import LoxRuntimeError
from lox.token_type import Token


class Environment:
    def __init__(self):
        self.values: dict[str, object] = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        else:
            raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
