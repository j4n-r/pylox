from pathlib import Path

ast_defs = {
    "Binary": [("Expr", "left"), ("Token", "operator"), ("Expr", "right")],
    "Grouping": [("Expr", "expression")],
    "Literal": [("object", "value")],
    "Unary": [("Token", "operator"), ("Expr", "right")],
}

code = """from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Protocol

from .token import Token


@dataclass
class Expr:
    pass
    
    class Visitor(Protocol):
"""

path = Path(__file__).parent / "../lox/ast_types.py"
path.parent.mkdir(parents=True, exist_ok=True)

with open(path, "w") as f:
    f.write(code)

    # Visitor methods
    for expr in ast_defs.keys():
        f.write(
            f"        def visit_{expr.lower()}_expr(self, expr: {expr}) -> object: ...\n"
        )
    f.write("\n")

    # AST classes
    for expr, fields in ast_defs.items():
        f.write("@dataclass\n")
        f.write(f"class {expr}(Expr):\n")

        for field_type, field_name in fields:
            f.write(f"    {field_name}: Final[{field_type}]\n")

        f.write("\n    def accept(self, visitor: Expr.Visitor) -> object:\n")
        f.write(f"        return visitor.visit_{expr.lower()}_expr(self)\n")
        f.write("\n")

print(f"Generated AST types at: {path.resolve()}")
