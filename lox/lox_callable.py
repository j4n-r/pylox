from typing import Protocol

from lox.interpreter import Interpreter


class LoxCallable(Protocol):
    def arity(self) -> int: ...
    def call(self, interpreter: Interpreter, arguments: list[object]) -> object: ...
