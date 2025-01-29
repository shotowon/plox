from typing import List, Iterator, Any

from tokens import Token, TokenType


class Scanner:
    def __init__(self, source: str):
        self.__source = source
        self.__tokens: List[Token] = []
        self.__start = 0
        self.__current = 0
        self.__line = 1

    def scan_token(self) -> Token:
        token: Token = self.__new_token()
        char: str | None = self.__advance()
        while char is not None and char.isspace():
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
            case None:
                token = self.__new_token(TokenType.EOF)

        self.__start = self.__current
        self.__tokens.append(token)
        return token

    def __advance(self) -> str | None:
        if self.__is_source_end():
            return None
        self.__current += 1
        return self.__source[self.__current - 1]

    def __is_source_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __new_token(
        self,
        type: TokenType = TokenType.EOF,
        literal: Any = None,
    ) -> Token:
        lexeme: str = self.__source[self.__start : self.__current]
        return Token(
            type=type,
            lexeme=lexeme,
            literal=literal,
            line=self.__line,
        )

    def __iter__(self) -> Iterator[Token]:
        return self

    def __next__(self) -> Token:
        if len(self.__tokens) != 0 and self.__tokens[-1].type == TokenType.EOF:
            raise StopIteration
        token = self.scan_token()
        return token
