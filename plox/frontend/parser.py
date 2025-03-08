from plox.frontend.tokens import Token, TokenType as TT
from plox.frontend.ast import (
    Expr,
    GroupingExpr,
    LiteralExpr,
    UnaryExpr,
    BinaryExpr,
    Stmt,
    ExpressionStmt,
    PrintStmt,
)


class ParseException(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token: Token = token
        self.message: str = message
        super().__init__(str(self))

    def __str__(self) -> str:
        return f"{self.token}: parse error - {self.message}"


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.__current = 0

    def parse(self) -> list[Stmt]:
        stmts: list[Stmt] = []
        while not self.__is_at_end():
            stmts.append(self.__stmt())
        return stmts

    def __stmt(self) -> Stmt:
        if self.__match(TT.PRINT):
            return self.__print_stmt()
        return self.__expr_stmt()

    def __print_stmt(self) -> PrintStmt:
        expr: Expr = self.__expr()
        self.__consume(TT.SEMICOLON, "Expect ';' after print value")
        return PrintStmt(expr)

    def __expr_stmt(self) -> ExpressionStmt:
        expr: Expr = self.__expr()
        self.__consume(TT.SEMICOLON, "Expect ';' after expr")
        return ExpressionStmt(expr)

    def __expr(self) -> Expr:
        return self.__eq()

    def __eq(self) -> Expr:
        expr: Expr = self.__comparison()

        while self.__match(TT.BANG_EQ, TT.EQ_EQ):
            op: Token = self.__previous()
            right: Expr = self.__comparison()
            expr = BinaryExpr(left=expr, operator=op, right=right)

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
            expr = BinaryExpr(expr, op, right)

        return expr

    def __term(self) -> Expr:
        expr: Expr = self.__factor()

        while self.__match(TT.PLUS, TT.MINUS):
            op: Token = self.__previous()
            right: Expr = self.__factor()
            expr = BinaryExpr(expr, op, right)

        return expr

    def __factor(self) -> Expr:
        expr: Expr = self.__unary()

        while self.__match(TT.STAR, TT.SLASH):
            op: Token = self.__previous()
            right: Expr = self.__unary()
            expr = BinaryExpr(expr, op, right)
        return expr

    def __unary(self) -> Expr:
        if self.__match(TT.BANG, TT.MINUS):
            op: Token = self.__previous()
            right: Expr = self.__unary()
            return UnaryExpr(op, right)
        return self.__primary()

    def __primary(self) -> Expr:
        if self.__match(TT.FALSE):
            return LiteralExpr(False)
        if self.__match(TT.TRUE):
            return LiteralExpr(True)
        if self.__match(TT.NIL):
            return LiteralExpr(None)
        if self.__match(TT.NUMBER, TT.STRING):
            return LiteralExpr(self.__previous().literal)

        if self.__match(TT.LPAREN):
            expr: Expr = self.__expr()
            self.__consume(TT.RPAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise self.__err(message="Expect expression.")

    def __consume(self, token_type: TT, message: str) -> Token:
        if self.__check(token_type=token_type):
            return self.__advance()

        raise self.__err(message=message)

    def __sync(self) -> None:
        self.__advance()

        while not self.__is_at_end():
            if (
                self.__previous().type == TT.SEMICOLON
                or self.__peek().type
                in [
                    TT.CLASS,
                    TT.FUN,
                    TT.VAR,
                    TT.FOR,
                    TT.IF,
                    TT.WHILE,
                    TT.PRINT,
                    TT.RETURN,
                ]
            ):
                return

            self.__advance()

    def __err(self, message: str) -> ParseException:
        return ParseException(token=self.__peek(), message=message)

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
