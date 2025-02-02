from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from dataclasses import dataclass

from plox.tokens import Token


T = TypeVar("T")


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: "ExprVisitor[T]") -> T:
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitBinaryExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitGroupingExpr(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitLiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitUnaryExpr(self)


R = TypeVar("R")


class ExprVisitor(Generic[R], ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary) -> R:
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping) -> R:
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal) -> R:
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary) -> R:
        pass
