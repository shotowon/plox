from typing import TYPE_CHECKING, Any, Optional
from abc import ABC, abstractmethod

from plox.frontend.ast import BlockStmt, FunctionStmt
from plox.frontend.tokens import Token

if TYPE_CHECKING:
    from plox.backend.visitors.eval.visitor import Eval


class Return(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value


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


class LoxFunction(LoxCallable):
    def __init__(self, decl: FunctionStmt) -> None:
        if not isinstance(decl.body, BlockStmt):
            raise RuntimeException(
                decl.name, "function definition's body must be block statement."
            )
        self.__decl = decl

    def call(self, eval: "Eval", args: list[Any]) -> Any:
        values: dict[str, Any] = {}
        for i, param in enumerate(self.__decl.params):
            values[param.lexeme] = args[i]

        if not isinstance(self.__decl.body, BlockStmt):
            raise RuntimeException(
                self.__decl.name, "function definition's body must be block statement."
            )

        try:
            eval.exec_block(self.__decl.body.statements, values)
        except Return as ret:
            return ret.value

        return None

    def arity(self) -> int:
        return len(self.__decl.params)


class RuntimeException(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message
