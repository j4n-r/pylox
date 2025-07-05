from __future__ import annotations
from lox.lox_callable import LoxCallable
from lox.stmt_types import Function


class LoxFunction(LoxCallable):
    def __init__(self, declaration : Function) -> None:
        
