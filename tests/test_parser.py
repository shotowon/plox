from plox.frontend.scanner import Scanner
from plox.frontend.parser import Parser
from plox.frontend.tokens import TokenType as TT, Token
from plox.frontend import ast


class TestParser:
    def test_exprs(self) -> None:
        srcs: list[str] = [
            "2 - 3 + 4",
            "10 / 2 * 3",
            "5 > 3",
            "(1 + 2) * 3",
            "-4 + 5",
            "3 <= 2",
            '"hello" == "world"',
            "nil == 32",
        ]

        tests: list[ast.Expr] = [
            # 2 - 3 + 4
            ast.Binary(
                ast.Binary(
                    ast.Literal(2),
                    Token(TT.MINUS, "-", None, 1),
                    ast.Literal(3),
                ),
                Token(TT.PLUS, "+", None, 1),
                ast.Literal(4),
            ),
            # 10 / 2 * 3
            ast.Binary(
                ast.Binary(
                    ast.Literal(10),
                    Token(TT.SLASH, "/", None, 1),
                    ast.Literal(2),
                ),
                Token(TT.STAR, "*", None, 1),
                ast.Literal(3),
            ),
            # 5 > 3
            ast.Binary(
                ast.Literal(5),
                Token(TT.GT, ">", None, 1),
                ast.Literal(3),
            ),
            # (1 + 2) * 3
            ast.Binary(
                ast.Grouping(
                    ast.Binary(
                        ast.Literal(1),
                        Token(TT.PLUS, "+", None, 1),
                        ast.Literal(2),
                    )
                ),
                Token(TT.STAR, "*", None, 1),
                ast.Literal(3),
            ),
            # -4 + 5
            ast.Binary(
                ast.Unary(
                    Token(TT.MINUS, "-", None, 1),
                    ast.Literal(4),
                ),
                Token(TT.PLUS, "+", None, 1),
                ast.Literal(5),
            ),
            # 3 <= 2
            ast.Binary(
                ast.Literal(3),
                Token(TT.LTE, "<=", None, 1),
                ast.Literal(2),
            ),
            ast.Binary(
                ast.Literal("hello"),
                Token(TT.EQ_EQ, "==", None, 1),
                ast.Literal("world"),
            ),
            ast.Binary(
                ast.Literal(None),
                Token(TT.EQ_EQ, "==", None, 1),
                ast.Literal(32),
            ),
        ]

        for src, expected in zip(srcs, tests):
            tokens = [token for token in Scanner(src)]
            parser: Parser = Parser(tokens=tokens)

            got: ast.Expr = parser.parse()
            assert got == expected
