from typing import Any
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    EOF = auto()

    # keywords
    CLASS = auto()
    SUPER = auto()
    THIS = auto()
    FUN = auto()
    VAR = auto()
    PRINT = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    AND = auto()
    OR = auto()
    TRUE = auto()
    FALSE = auto()

    # literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    NIL = auto()

    # one or two char tokens
    BANG = auto()
    BANG_EQ = auto()
    EQ = auto()
    EQ_EQ = auto()
    GT = auto()
    GTE = auto()
    LT = auto()
    LTE = auto()

    # single char
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    DOT = auto()
    COMMA = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    STAR = auto()
    SLASH = auto()

    # special tokens
    INVALID = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int
    meta: str = ""

    def __str__(self) -> str:
        return f"'{self.type}' '{self.lexeme}' '{self.literal}'"


keywords = {
    "class": TokenType.CLASS,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "fun": TokenType.FUN,
    "var": TokenType.VAR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "nil": TokenType.NIL,
}
