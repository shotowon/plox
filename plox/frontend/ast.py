from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

from plox.frontend.tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        pass


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitBinaryExpr(self)


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitGroupingExpr(self)


@dataclass
class LiteralExpr(Expr):
    value: Any = None

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitLiteralExpr(self)


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitUnaryExpr(self)


class ExprVisitor[R](ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr: BinaryExpr) -> R:
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: GroupingExpr) -> R:
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: LiteralExpr) -> R:
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: UnaryExpr) -> R:
        pass


class Stmt(ABC):
    @abstractmethod
    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        pass


@dataclass
class ExpressionStmt(Stmt):
    expression: Expr

    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        return visitor.visitExpressionStmt(self)


@dataclass
class PrintStmt(Stmt):
    expression: Expr

    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        return visitor.visitPrintStmt(self)


class StmtVisitor[R](ABC):
    @abstractmethod
    def visitExpressionStmt(self, stmt: ExpressionStmt) -> R:
        pass

    @abstractmethod
    def visitPrintStmt(self, stmt: PrintStmt) -> R:
        pass
