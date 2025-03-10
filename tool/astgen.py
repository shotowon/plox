"""
Script that generates AST classes based on definition provided by user
"""

import io
from pathlib import Path

import black


def main():
    try:
        output_dir = Path("plox/frontend")
        filename = "ast.py"

        if not output_dir.exists():
            output_dir.mkdir()

        filepath = output_dir / filename
        if not filepath.exists():
            filepath.touch()

        buf = io.StringIO()
        buf.write("from abc import ABC, abstractmethod\n")
        buf.write("from typing import Any\n")
        buf.write("from dataclasses import dataclass\n\n")
        buf.write("from plox.frontend.tokens import Token\n\n\n")

        define_ast(
            buf,
            "Expr",
            [
                "Assign   : Token name, Expr value",
                "Logical  : Expr left, Token operator, Expr right",
                "Binary   : Expr left, Token operator, Expr right",
                "Grouping : Expr expression",
                "Unary    : Token operator, Expr right",
                "Literal  : Any value",
                "Variable : Token name",
            ],
        )

        define_ast(
            buf,
            "Stmt",
            [
                "Block        : list[Stmt] statements",
                "Expression   : Expr expression",
                "If           : Expr condition, Stmt thenBranch, Stmt elseBranch",
                "Print        : Expr expression",
                "Var          : Token name, Expr initializer",
                "While        : Expr condition, Stmt body",
            ],
        )

        file_contents = black.format_str(buf.getvalue(), mode=black.FileMode())
        filepath.write_text(file_contents)
    except Exception as e:
        print(e)


def define_ast(
    buf: io.StringIO,
    basename: str,
    types: list[str],
):

    buf.write(f"class {basename}(ABC):\n")
    buf.write(f"    @abstractmethod\n")
    buf.write(
        f"    def accept[T](self, visitor: '{basename}Visitor[T]') -> T:\n"
    )
    buf.write(f"        pass\n\n")

    expr_defs = [list(map(lambda l: l.strip(), t.split(":"))) for t in types]

    for classname, fields in expr_defs:
        define_type(buf, basename, classname, fields)

    define_visitor(
        buf,
        basename,
        list(map(lambda clasdef: clasdef[0], expr_defs)),
    )


def define_type(
    buf: io.TextIOBase,
    basename: str,
    classname: str,
    fields: str,
) -> None:
    buf.write("@dataclass\n")
    buf.write(f"class {classname}{basename}({basename}):\n")
    for field in map(lambda s: s.strip(), fields.split(",")):
        field_type, field_name = field.split()
        buf.write(f"    {field_name}: {field_type}")
        if field_type == "Any":
            buf.write(" = None")
        buf.write("\n")

    buf.write(
        f"    def accept[T](self, visitor: '{basename}Visitor[T]') -> T:\n"
    )
    buf.write(f"        return visitor.visit{classname}{basename}(self)\n\n")
    buf.write("\n\n")


def define_visitor(
    buf: io.TextIOBase,
    basename: str,
    classnames: list[str],
) -> None:
    buf.write(f"class {basename}Visitor[R](ABC):\n")

    for classname in classnames:
        buf.write(f"    @abstractmethod\n")
        buf.write(f"    def ")
        buf.write(f"visit{classname}{basename}")
        buf.write(f"(self, {basename.lower()}: {classname}{basename}) -> R:\n")
        buf.write(f"        pass\n\n")


main()
