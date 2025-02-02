"""
Script that generates AST classes based on definition provided by user
"""

import sys
import io
from pathlib import Path
from typing import List

import black


def main():
    try:
        output_dir = Path("plox/ast")
        filename = "ast.py"
        basename = "Expr"

        define_ast(
            output_dir,
            filename,
            basename,
            [
                "Binary   : Expr left, Token operator, Expr right",
                "Grouping : Expr expression",
                "Literal  : Any value",
                "Unary    : Token operator, Expr right",
            ],
        )
    except Exception as e:
        print(e)


def define_ast(
    output_dir: Path,
    filename: str,
    basename: str,
    types: List[str],
):
    if not output_dir.exists():
        output_dir.mkdir()

    filepath = output_dir / filename
    if not filepath.exists():
        filepath.touch()

    buf = io.StringIO()
    buf.write("from abc import ABC, abstractmethod\n")
    buf.write("from typing import Any, Generic, TypeVar\n")
    buf.write("from dataclasses import dataclass\n\n")
    buf.write("from plox.tokens import Token\n\n\n")

    buf.write(f'T = TypeVar("T")\n\n')
    buf.write(f"class {basename}(ABC):\n")
    buf.write(f"    @abstractmethod\n")
    buf.write(f"    def accept(self, visitor: '{basename}Visitor[T]') -> T:\n")
    buf.write(f"        pass\n\n")

    expr_defs = [list(map(lambda l: l.strip(), t.split(":"))) for t in types]

    for classname, fields in expr_defs:
        define_type(buf, basename, classname, fields)

    define_visitor(
        buf,
        basename,
        list(map(lambda clasdef: clasdef[0], expr_defs)),
    )

    file_contents = black.format_str(buf.getvalue(), mode=black.FileMode())

    filepath.write_text(file_contents)


def define_type(
    buf: io.TextIOBase,
    basename: str,
    classname: str,
    fields: str,
) -> None:
    buf.write("@dataclass\n")
    buf.write(f"class {classname}({basename}):\n")
    for field in map(lambda s: s.strip(), fields.split(",")):
        field_type, field_name = field.split()
        buf.write(f"    {field_name}: {field_type}\n")

    buf.write(f"    def accept(self, visitor: '{basename}Visitor[T]') -> T:\n")
    buf.write(f"        return visitor.visit{classname}{basename}(self)\n\n")
    buf.write("\n\n")


def define_visitor(
    buf: io.TextIOBase,
    basename: str,
    classnames: List[str],
) -> None:
    buf.write(f'R = TypeVar("R")\n\n')
    buf.write(f"class {basename}Visitor(Generic[R], ABC):\n")

    for classname in classnames:
        buf.write(f"    @abstractmethod\n")
        buf.write(f"    def ")
        buf.write(f"visit{classname}{basename}")
        buf.write(f"(self, {basename.lower()}: {classname}) -> R:\n")
        buf.write(f"        pass\n\n")


main()
