from enum import Enum, auto


class TokenType(Enum):
    EOF = auto()

    # keywords
    CLASS = auto()
    SUPER = auto()
    THIS = auto()
    FUN = auto()
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
