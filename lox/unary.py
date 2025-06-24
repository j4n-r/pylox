from dataclasses import dataclass
from typing import Final

from .token import Token


@dataclass
class Expr:
    pass


@dataclass
class Unary(Expr):
    operator: Final[Token] | None
    right: Final[Expr] | None
