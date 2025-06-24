ast_defs = {
    "Binary": {"Expr": "left", "Token": "operator", "Expr": "right"},
    "Grouping": {"Expr": "expression"},
    "Literal": {"object": " value"},
    "Unary": {"Token": "operator", "Expr": "right"},
}

code = """
from dataclasses import dataclass
from typing import Final

from .token import Token


@dataclass
class Expr:
    pass

"""

with open("../lox/ast_types.py", "w") as f:
    f.write(code)
    for expr, dicts in ast_defs.items():
        f.write("@dataclass\n")
        f.write(f"class {expr}(Expr):\n")
        for type, var in dicts.items():
            f.write(f"    {var}: Final[{type}] | None\n")
        f.write("\n")
