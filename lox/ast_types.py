from dataclasses import dataclass
from typing import Final

from .token import Token


@dataclass
class Expr:
    pass


@dataclass
class Binary(Expr):
    right: Final[Expr] | None
    operator: Final[Token] | None


@dataclass
class Grouping(Expr):
    expression: Final[Expr] | None


@dataclass
class Literal(Expr):
    value: Final[object] | None


@dataclass
class Unary(Expr):
    operator: Final[Token] | None
    right: Final[Expr] | None
