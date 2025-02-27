from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

from plox.frontend.tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitBinaryExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitGroupingExpr(self)


@dataclass
class Literal(Expr):
    value: Any = None

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitLiteralExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitUnaryExpr(self)


class ExprVisitor[R](ABC):
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
