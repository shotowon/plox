from plox.frontend.scanner import Scanner
from plox.frontend.parser import Parser
from plox.frontend.tokens import TokenType as TT, Token
from plox.frontend import ast


class TestParser:
    def test_exprs(self) -> None:
        srcs: list[str] = [
            "2 - 3 + 4;",
            "10 / 2 * 3;",
            "5 > 3;",
            "(1 + 2) * 3;",
            "-4 + 5;",
            "3 <= 2;",
            '"hello" == "world";',
            "nil == 32;",
        ]

        tests: list[ast.Expr] = [
            # 2 - 3 + 4
            ast.BinaryExpr(
                ast.BinaryExpr(
                    ast.LiteralExpr(2),
                    Token(TT.MINUS, "-", None, 1),
                    ast.LiteralExpr(3),
                ),
                Token(TT.PLUS, "+", None, 1),
                ast.LiteralExpr(4),
            ),
            # 10 / 2 * 3
            ast.BinaryExpr(
                ast.BinaryExpr(
                    ast.LiteralExpr(10),
                    Token(TT.SLASH, "/", None, 1),
                    ast.LiteralExpr(2),
                ),
                Token(TT.STAR, "*", None, 1),
                ast.LiteralExpr(3),
            ),
            # 5 > 3
            ast.BinaryExpr(
                ast.LiteralExpr(5),
                Token(TT.GT, ">", None, 1),
                ast.LiteralExpr(3),
            ),
            # (1 + 2) * 3
            ast.BinaryExpr(
                ast.GroupingExpr(
                    ast.BinaryExpr(
                        ast.LiteralExpr(1),
                        Token(TT.PLUS, "+", None, 1),
                        ast.LiteralExpr(2),
                    )
                ),
                Token(TT.STAR, "*", None, 1),
                ast.LiteralExpr(3),
            ),
            # -4 + 5
            ast.BinaryExpr(
                ast.UnaryExpr(
                    Token(TT.MINUS, "-", None, 1),
                    ast.LiteralExpr(4),
                ),
                Token(TT.PLUS, "+", None, 1),
                ast.LiteralExpr(5),
            ),
            # 3 <= 2
            ast.BinaryExpr(
                ast.LiteralExpr(3),
                Token(TT.LTE, "<=", None, 1),
                ast.LiteralExpr(2),
            ),
            ast.BinaryExpr(
                ast.LiteralExpr("hello"),
                Token(TT.EQ_EQ, "==", None, 1),
                ast.LiteralExpr("world"),
            ),
            ast.BinaryExpr(
                ast.LiteralExpr(None),
                Token(TT.EQ_EQ, "==", None, 1),
                ast.LiteralExpr(32),
            ),
        ]

        for src, expected in zip(srcs, tests):
            tokens = [token for token in Scanner(src)]
            parser: Parser = Parser(tokens=tokens)

            stmts: list[ast.Stmt] = parser.parse()
            assert len(stmts) == 1
            got = stmts[0]
            assert (
                isinstance(got, ast.ExpressionStmt)
                and got.expression == expected
            )
