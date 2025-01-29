from typing import List

from tokens import Token


class Scanner:
    def __init__(self, source: str):
        self.__source = source
        self.__tokens: List[Token] = []
        self.__start = 0
        self.__current = 0
        self.__line = 1
