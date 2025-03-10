from plox.frontend.tokens import Token, TokenType as TT
from plox.frontend.ast import (
    Expr,
    AssignExpr,
    GroupingExpr,
    LiteralExpr,
    LogicalExpr,
    UnaryExpr,
    BinaryExpr,
    VariableExpr,
    Stmt,
    ExpressionStmt,
    IfStmt,
    BlockStmt,
    PrintStmt,
    VarStmt,
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
        self.errors: list[ParseException] = []
        self.__tokens = tokens
        self.__current = 0

    def parse(self) -> list[Stmt]:
        stmts: list[Stmt] = []
        while not self.__is_at_end():
            if (decl_or_stmt := self.__decl()) is not None:
                stmts.append(decl_or_stmt)
        return stmts

    def more_tokens(self, tokens: list[Token]) -> None:
        if len(self.__tokens) != 0:
            self.__tokens.pop()
        self.__tokens.extend(tokens)
        self.__current = 0
        self.errors = []

    def __decl(self) -> Stmt | None:
        try:
            if self.__match(TT.VAR):
                return self.__var_decl()
            return self.__stmt()
        except ParseException as e:
            self.__sync()
            self.errors.append(e)

    def __var_decl(self) -> Stmt:
        name: Token = self.__consume(TT.IDENTIFIER, "Expect variable name.")

        initializer: Expr = LiteralExpr()
        if self.__match(TT.EQ):
            initializer = self.__expr()
        self.__consume(
            TT.SEMICOLON,
            "Expect ';' after variable declaration.",
        )
        return VarStmt(name=name, initializer=initializer)

    def __stmt(self) -> Stmt:
        if self.__match(TT.IF):
            return self.__if_stmt()
        if self.__match(TT.PRINT):
            return self.__print_stmt()
        if self.__match(TT.LBRACE):
            return self.__block_stmt()
        return self.__expr_stmt()

    def __print_stmt(self) -> Stmt:
        expr: Expr = self.__expr()
        self.__consume(TT.SEMICOLON, "Expect ';' after print value.")
        return PrintStmt(expr)

    def __if_stmt(self) -> Stmt:
        self.__consume(TT.LPAREN, "Expect '(' after 'if'.")
        condition: Expr = self.__expr()
        self.__consume(TT.RPAREN, "Expect ')' after condition in 'if'.")
        thenStmt: Stmt = self.__stmt()

        elseBranch = ExpressionStmt(LiteralExpr(None))
        if self.__match(TT.ELSE):
            elseBranch = self.__stmt()

        return IfStmt(
            condition=condition,
            thenBranch=thenStmt,
            elseBranch=elseBranch,
        )

    def __expr_stmt(self) -> Stmt:
        expr: Expr = self.__expr()
        self.__consume(TT.SEMICOLON, "Expect ';' after expr.")
        return ExpressionStmt(expr)

    def __block_stmt(self) -> Stmt:
        stmts: list[Stmt] = []

        while not self.__check(TT.RBRACE) and not self.__is_at_end():
            if (decl_or_stmt := self.__decl()) is not None:
                stmts.append(decl_or_stmt)
        self.__consume(TT.RBRACE, "Expect '}' after block.")
        return BlockStmt(stmts)

    def __expr(self) -> Expr:
        return self.__assign()

    def __assign(self) -> Expr:
        expr: Expr = self.__or()

        if self.__match(TT.EQ):
            value: Expr = self.__assign()

            if isinstance(expr, VariableExpr):
                name: Token = expr.name
                return AssignExpr(name, value)

            self.__err("Invalid assignment target.")
        return expr

    def __or(self) -> Expr:
        expr: Expr = self.__and()

        while self.__match(TT.OR):
            op: Token = self.__previous()
            right: Expr = self.__and()
            expr = LogicalExpr(left=expr, operator=op, right=right)

        return expr

    def __and(self) -> Expr:
        expr: Expr = self.__eq()

        while self.__match(TT.AND):
            op: Token = self.__previous()
            right: Expr = self.__eq()
            expr = LogicalExpr(left=expr, operator=op, right=right)
        return expr

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

        if self.__match(TT.IDENTIFIER):
            return VariableExpr(self.__previous())

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
