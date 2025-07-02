from __future__ import annotations

from typing import Optional

from lox.errors import LoxRuntimeError
from lox.token_type import Token


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None):
        self.values: dict[str, object] = {}
        self.enclosing = enclosing

    def define(self, name: str, value: object):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        else:
            raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable {name.lexeme}.")
