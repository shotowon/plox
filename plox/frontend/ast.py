from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

from plox.frontend.tokens import Token


class Expr(ABC):
    @abstractmethod
    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        pass


@dataclass
class AssignExpr(Expr):
    name: Token
    value: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitAssignExpr(self)


@dataclass
class LogicalExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitLogicalExpr(self)


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
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitUnaryExpr(self)


@dataclass
class LiteralExpr(Expr):
    value: Any = None

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitLiteralExpr(self)


@dataclass
class VariableExpr(Expr):
    name: Token

    def accept[T](self, visitor: "ExprVisitor[T]") -> T:
        return visitor.visitVariableExpr(self)


class ExprVisitor[R](ABC):
    @abstractmethod
    def visitAssignExpr(self, expr: AssignExpr) -> R:
        pass

    @abstractmethod
    def visitLogicalExpr(self, expr: LogicalExpr) -> R:
        pass

    @abstractmethod
    def visitBinaryExpr(self, expr: BinaryExpr) -> R:
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: GroupingExpr) -> R:
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: UnaryExpr) -> R:
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: LiteralExpr) -> R:
        pass

    @abstractmethod
    def visitVariableExpr(self, expr: VariableExpr) -> R:
        pass


class Stmt(ABC):
    @abstractmethod
    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        pass


@dataclass
class BlockStmt(Stmt):
    statements: list[Stmt]

    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        return visitor.visitBlockStmt(self)


@dataclass
class ExpressionStmt(Stmt):
    expression: Expr

    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        return visitor.visitExpressionStmt(self)


@dataclass
class IfStmt(Stmt):
    condition: Expr
    thenBranch: Stmt
    elseBranch: Stmt

    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        return visitor.visitIfStmt(self)


@dataclass
class PrintStmt(Stmt):
    expression: Expr

    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        return visitor.visitPrintStmt(self)


@dataclass
class VarStmt(Stmt):
    name: Token
    initializer: Expr

    def accept[T](self, visitor: "StmtVisitor[T]") -> T:
        return visitor.visitVarStmt(self)


class StmtVisitor[R](ABC):
    @abstractmethod
    def visitBlockStmt(self, stmt: BlockStmt) -> R:
        pass

    @abstractmethod
    def visitExpressionStmt(self, stmt: ExpressionStmt) -> R:
        pass

    @abstractmethod
    def visitIfStmt(self, stmt: IfStmt) -> R:
        pass

    @abstractmethod
    def visitPrintStmt(self, stmt: PrintStmt) -> R:
        pass

    @abstractmethod
    def visitVarStmt(self, stmt: VarStmt) -> R:
        pass
