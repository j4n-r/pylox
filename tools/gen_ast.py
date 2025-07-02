from pathlib import Path


def define_ast(output_dir: str, base_name: str, types: list[str]):
    """
    Generate AST classes for a given base type.

    Args:
        output_dir: Directory to write the file
        base_name: Base class name (e.g., "Expr", "Stmt")
        types: List of type definitions in format "ClassName : field_type field_name, ..."
    """
    # Parse type definitions
    ast_defs = {}
    for type_def in types:
        class_name, fields_str = type_def.split(" : ")
        class_name = class_name.strip()

        if fields_str.strip():
            # Split by comma and parse each field
            fields = []
            for field in fields_str.split(","):
                parts = field.strip().split()
                if len(parts) == 2:
                    field_type, field_name = parts
                    fields.append((field_type, field_name))
            ast_defs[class_name] = fields
        else:
            ast_defs[class_name] = []

    # Generate code
    code = f"""from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from lox.token_type import Token
"""

    # Add Expr import if we're generating Stmt
    if base_name == "Stmt":
        code += "from lox.expr_types import Expr\n"

    code += f"""

@dataclass
class {base_name}(ABC):
    pass
    
    @abstractmethod
    def accept[R](self, visitor: {base_name}.Visitor[R]) -> R:
        pass

    class Visitor[R](Protocol):
"""

    # Write to file
    output_path = Path(output_dir) / f"{base_name.lower()}_types.py"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(code)

        # Visitor methods
        for class_name in ast_defs.keys():
            method_name = f"visit_{class_name.lower()}_{base_name.lower()}"
            f.write(
                f"        def {method_name}(self, {base_name.lower()}: {class_name}) -> R: ...\n"
            )
        f.write("\n")

        # AST classes
        for class_name, fields in ast_defs.items():
            f.write("@dataclass\n")
            f.write(f"class {class_name}({base_name}):\n")

            if fields:
                for field_type, field_name in fields:
                    f.write(f"    {field_name}: {field_type}\n")
            else:
                f.write("    pass\n")

            f.write(
                f"\n    def accept[R](self, visitor: {base_name}.Visitor[R]) -> R:\n"
            )
            method_name = f"visit_{class_name.lower()}_{base_name.lower()}"
            f.write(f"        return visitor.{method_name}(self)\n")
            f.write("\n")

    print(f"Generated {base_name} types at: {output_path.resolve()}")


# Usage examples:

# Generate expressions
expr_types = [
    "Assign   : Token name, Expr value",
    "Binary   : Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal  : object value",
    "Logical  : Expr left, Token operator, Expr right",
    "Unary    : Token operator, Expr right",
    "Variable : Token name",
]

define_ast("lox", "Expr", expr_types)

# Generate statements
stmt_types = [
    "Block      : list[Stmt] statements",
    "Expression : Expr expression",
    "Print      : Expr expression",
    "If         : Expr condition, Stmt then_branch," + " Stmt else_branch",
    "Var        : Token name, Expr initializer",
    "While      : Expr condition, Stmt body",
]

define_ast("lox", "Stmt", stmt_types)
