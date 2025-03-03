from plox.frontend.scanner import Scanner
from plox.frontend.parser import Parser
from plox.frontend.tokens import TokenType as TT, Token
from plox.frontend import ast


class TestParser:
    def test_exprs(self) -> None:
        scanner: Scanner = Scanner("2 + 3 * 4")
        tokens = [token for token in scanner]
        parser: Parser = Parser(tokens=tokens)

        expr: ast.Expr = parser.parse()
        expected: ast.Expr = ast.Binary(
            ast.Literal(2),
            Token(TT.PLUS, "+", None, 1),
            ast.Binary(
                ast.Literal(3), Token(TT.STAR, "*", None, 1), ast.Literal(4)
            ),
        )
        assert expected == expr
