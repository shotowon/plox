from typing import List

from plox.frontend.scanner import Scanner
from plox.frontend.tokens import TokenType, Token


class TestScanner:
    def test_function_declaration(self) -> None:
        source = """fun main() {
    var x = 132;
    var y = 123213.232;
    print "Hello, World!";
}
"""
        expected_tokens: List[Token] = [
            Token(type=TokenType.FUN, lexeme="fun", line=1, literal=None),
            Token(
                type=TokenType.IDENTIFIER, lexeme="main", line=1, literal=None
            ),
            Token(type=TokenType.LPAREN, lexeme="(", line=1, literal=None),
            Token(type=TokenType.RPAREN, lexeme=")", line=1, literal=None),
            Token(type=TokenType.LBRACE, lexeme="{", line=1, literal=None),
            Token(type=TokenType.VAR, lexeme="var", line=2, literal=None),
            Token(type=TokenType.IDENTIFIER, lexeme="x", line=2, literal=None),
            Token(type=TokenType.EQ, lexeme="=", line=2, literal=None),
            Token(type=TokenType.NUMBER, lexeme="132", line=2, literal=132),
            Token(type=TokenType.SEMICOLON, lexeme=";", line=2, literal=None),
            Token(type=TokenType.VAR, lexeme="var", line=3, literal=None),
            Token(type=TokenType.IDENTIFIER, lexeme="y", line=3, literal=None),
            Token(type=TokenType.EQ, lexeme="=", line=3, literal=None),
            Token(
                type=TokenType.NUMBER,
                lexeme="123213.232",
                line=3,
                literal=123213.232,
            ),
            Token(type=TokenType.SEMICOLON, lexeme=";", line=3, literal=None),
            Token(type=TokenType.PRINT, lexeme="print", line=4, literal=None),
            Token(
                type=TokenType.STRING,
                lexeme='"Hello, World!"',
                line=4,
                literal="Hello, World!",
            ),
            Token(type=TokenType.SEMICOLON, lexeme=";", line=4, literal=None),
            Token(type=TokenType.RBRACE, lexeme="}", line=5, literal=None),
            Token(type=TokenType.EOF, lexeme="", line=6, literal=None),
        ]
        scanner: Scanner = Scanner(source=source)

        for expected_token in expected_tokens:
            token = next(scanner)
            assert (
                token.type == expected_token.type
                and token.lexeme == expected_token.lexeme
                and token.literal == expected_token.literal
                and token.line == expected_token.line
            )

    def test_class_declaration(self) -> None:
        source = """class Breakfast {
    cook() {
        print "Eggs a-fryin'!";
    }

    serve(who) {
        print "Enjoy your breakfast, " + who + ".";
    }
}
"""

        expected_tokens: List[Token] = [
            Token(type=TokenType.CLASS, lexeme="class", line=1, literal=None),
            Token(
                type=TokenType.IDENTIFIER,
                lexeme="Breakfast",
                line=1,
                literal=None,
            ),
            Token(type=TokenType.LBRACE, lexeme="{", line=1, literal=None),
            Token(
                type=TokenType.IDENTIFIER,
                lexeme="cook",
                line=2,
                literal=None,
            ),
            Token(type=TokenType.LPAREN, lexeme="(", line=2, literal=None),
            Token(type=TokenType.RPAREN, lexeme=")", line=2, literal=None),
            Token(type=TokenType.LBRACE, lexeme="{", line=2, literal=None),
            Token(type=TokenType.PRINT, lexeme="print", line=3, literal=None),
            Token(
                type=TokenType.STRING,
                lexeme='"Eggs a-fryin\'!"',
                line=3,
                literal="Eggs a-fryin'!",
            ),
            Token(type=TokenType.SEMICOLON, lexeme=";", line=3, literal=None),
            Token(type=TokenType.RBRACE, lexeme="}", line=4, literal=None),
            Token(
                type=TokenType.IDENTIFIER,
                lexeme="serve",
                line=6,
                literal=None,
            ),
            Token(type=TokenType.LPAREN, lexeme="(", line=6, literal=None),
            Token(
                type=TokenType.IDENTIFIER, lexeme="who", line=6, literal=None
            ),
            Token(type=TokenType.RPAREN, lexeme=")", line=6, literal=None),
            Token(type=TokenType.LBRACE, lexeme="{", line=6, literal=None),
            Token(type=TokenType.PRINT, lexeme="print", line=7, literal=None),
            Token(
                type=TokenType.STRING,
                lexeme='"Enjoy your breakfast, "',
                line=7,
                literal="Enjoy your breakfast, ",
            ),
            Token(type=TokenType.PLUS, lexeme="+", line=7, literal=None),
            Token(
                type=TokenType.IDENTIFIER, lexeme="who", line=7, literal=None
            ),
            Token(type=TokenType.PLUS, lexeme="+", line=7, literal=None),
            Token(
                type=TokenType.STRING,
                lexeme='"."',
                line=7,
                literal=".",
            ),
            Token(type=TokenType.SEMICOLON, lexeme=";", line=7, literal=None),
            Token(type=TokenType.RBRACE, lexeme="}", line=8, literal=None),
            Token(type=TokenType.RBRACE, lexeme="}", line=9, literal=None),
            Token(type=TokenType.EOF, lexeme="", line=10, literal=None),
        ]

        scanner: Scanner = Scanner(source=source)

        for expected_token in expected_tokens:
            token = next(scanner)
            assert (
                token.type == expected_token.type
                and token.lexeme == expected_token.lexeme
                and token.literal == expected_token.literal
                and token.line == expected_token.line
            )
