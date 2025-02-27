from plox.frontend.tokens import Token, TokenType as TT
from plox.frontend.ast import Expr, Grouping, Literal, Unary, Binary


class ParseException(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.__current = 0

    def __expr(self) -> Expr:
        return self.__eq()

    def __eq(self) -> Expr:
        expr: Expr = self.__comparison()

        while self.__match(TT.BANG_EQ, TT.EQ_EQ):
            op: Token = self.__previous()
            right: Expr = self.__comparison()
            expr = Binary(left=expr, operator=op, right=right)

        return expr

    def __comparison(self) -> Expr:
        expr: Expr = self.__term()

        while self.__match(
            TT.GT,
            TT.GTE,
            TT.LT,
            TT.LTE,
        ):
            op: Token = self.__previous()
            right: Expr = self.__term()
            expr = Binary(expr, op, right)

        return expr

    def __term(self) -> Expr:
        expr: Expr = self.__factor()

        while self.__match(TT.PLUS, TT.MINUS):
            op: Token = self.__previous()
            right: Expr = self.__factor()
            expr = Binary(expr, op, right)

        return expr

    def __factor(self) -> Expr:
        expr: Expr = self.__unary()

        while self.__match(TT.STAR, TT.SLASH):
            op: Token = self.__previous()
            right: Expr = self.__unary()
            expr = Binary(expr, op, right)
        return expr

    def __unary(self) -> Expr:
        if self.__match(TT.BANG, TT.MINUS):
            op: Token = self.__previous()
            right: Expr = self.__unary()
            return Unary(op, right)
        return self.__primary()

    def __primary(self) -> Expr:
        if self.__match(TT.FALSE):
            return Literal(False)
        if self.__match(TT.TRUE):
            return Literal(True)
        if self.__match(TT.NIL):
            return Literal(None)
        if self.__match(TT.NUMBER, TT.STRING):
            return Literal(self.__previous().literal)

        if self.__match(TT.LPAREN):
            expr: Expr = self.__expr()
            self.__consume(TT.RPAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.__err(message="Expect expression.")

    def __consume(self, token_type: TT, message: str) -> Token:
        if self.__check(token_type=token_type):
            return self.__advance()

        raise self.__err(message=message)

    def __err(self, message: str) -> ParseException:
        return ParseException(f"{self.__peek()}: {message}")

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.__current += 1
        return self.__previous()

    def __match(self, *token_types: TT) -> bool:
        for token_type in token_types:
            if self.__check(token_type):
                self.__advance()
                return True

        return False

    def __check(self, token_type: TT) -> bool:
        if self.__is_at_end():
            return False
        return self.__peek().type == token_type

    def __is_at_end(self) -> bool:
        return self.__peek().type == TT.EOF

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]
