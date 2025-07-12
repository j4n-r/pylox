from typing import Protocol, runtime_checkable


@runtime_checkable
class LoxCallable(Protocol):
    def arity(self) -> int: ...
    def call(self, interpreter, arguments: list[object]) -> object: ...
