from typing import TYPE_CHECKING, Any, Optional
from abc import ABC, abstractmethod

from plox.frontend.tokens import Token

if TYPE_CHECKING:
    from plox.backend.visitors.eval.visitor import Eval


class Context:
    def __init__(
        self,
        values: dict[str, Any] = {},
        parent: Optional["Context"] = None,
    ) -> None:
        self.parent = parent
        self.values = values

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.parent is not None:
            return self.parent.get(name)
        raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value


class LoxCallable(ABC):
    @abstractmethod
    def call(self, eval: "Eval", args: list[Any]) -> Any:
        pass

    @abstractmethod
    def arity(self) -> int:
        pass


class RuntimeException(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message
