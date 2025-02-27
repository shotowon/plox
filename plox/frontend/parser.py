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
