from typing import Iterator, Any

from plox.tokens import TokenType, Token


class Scanner:
    def __init__(self, source: str):
        self.__source = source
        self.__current_token: Token | None = None
        self.__start = 0
        self.__current = 0
        self.__line = 1

    def scan_token(self) -> Token:
        token: Token = self.__new_token()
        char: str = self.__advance()

        while char != "\0" and char.isspace():
            if char == "\n":
                self.__line += 1
            self.__start = self.__current
            char = self.__advance()

        match char:
            case "{":
                token = self.__new_token(TokenType.LBRACE)
            case "}":
                token = self.__new_token(TokenType.RBRACE)
            case "(":
                token = self.__new_token(TokenType.LPAREN)
            case ")":
                token = self.__new_token(TokenType.RPAREN)
            case ",":
                token = self.__new_token(TokenType.COMMA)
            case ".":
                token = self.__new_token(TokenType.DOT)
            case "+":
                token = self.__new_token(TokenType.PLUS)
            case "-":
                token = self.__new_token(TokenType.MINUS)
            case "*":
                token = self.__new_token(TokenType.STAR)
            case "/":
                token = self.__new_token(TokenType.SLASH)
            case ";":
                token = self.__new_token(TokenType.SEMICOLON)
            case "\0":
                token = self.__new_token(TokenType.EOF)

        self.__start = self.__current
        self.__current_token = token
        return token

    def __advance(self) -> str:
        if self.__is_source_end():
            return "\0"
        self.__current += 1
        return self.__source[self.__current - 1]


    def __match(self, next: str) -> bool:
        if self.__peek() != next and next != "\0":
            return False
        self.__current += 1
        return True

    def __peek(self, offset: int = 0) -> str:
        return (
            "\0"
            if self.__current + offset >= len(self.__source)
            else self.__source[self.__current + offset]
        )

    def __is_source_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __new_token(
        self,
        type: TokenType = TokenType.EOF,
        literal: Any = None,
        meta: str = "",
    ) -> Token:
        lexeme: str = self.__source[self.__start : self.__current]
        return Token(
            type=type,
            lexeme=lexeme,
            literal=literal,
            line=self.__line,
            meta=meta,
        )

    def __iter__(self) -> Iterator[Token]:
        return self

    def __next__(self) -> Token:
        if (
            self.__current_token is not None
            and self.__current_token.type == TokenType.EOF
        ):
            raise StopIteration
        token = self.scan_token()
        return token
