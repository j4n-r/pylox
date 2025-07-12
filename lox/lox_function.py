from __future__ import annotations

from typing import override

from lox.environment import Environment
from lox.lox_callable import LoxCallable
from lox.lox_return import LoxReturn
from lox.stmt_types import Function


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment) -> None:
        self.declaration = declaration
        self.closure = closure

    @override
    def call(self, interpreter, arguments: list[object]) -> object:
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except LoxReturn as returnValue:
            return returnValue.value
        return None

    @override
    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme} >"
