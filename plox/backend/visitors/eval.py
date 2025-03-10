from typing import Any, Optional
import copy

from plox.frontend.tokens import TokenType as TT, Token
from plox.frontend.ast import (
    Expr,
    AssignExpr,
    GroupingExpr,
    BinaryExpr,
    LogicalExpr,
    LiteralExpr,
    UnaryExpr,
    VariableExpr,
    Stmt,
    ExpressionStmt,
    IfStmt,
    WhileStmt,
    PrintStmt,
    VarStmt,
    BlockStmt,
    ExprVisitor,
    StmtVisitor,
)


class RuntimeException(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message


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


class Eval(ExprVisitor[Any], StmtVisitor[None]):
    def __init__(self, ctx: Context = Context()) -> None:
        self.ctx = ctx

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def eval(self, expr: Expr) -> Any:
        return expr.accept(visitor=self)

    # ExprVisitor

    def visitAssignExpr(self, expr: AssignExpr) -> Any:
        value: Any = self.eval(expr.value)
        self.ctx.assign(expr.name, value)
        return value

    def visitLiteralExpr(self, expr: LiteralExpr) -> Any:
        return expr.value

    def visitGroupingExpr(self, expr: GroupingExpr) -> Any:
        return self.eval(expr=expr.expression)

    def visitUnaryExpr(self, expr: UnaryExpr) -> Any:
        right: Any = self.eval(expr=expr.right)

        match expr.operator.type:
            case TT.MINUS:
                self.__check_num_un_operand(op=expr.operator, right=right)
                return -float(right)
            case TT.BANG:
                return not self.__bool_from_any(right)

        return None

    def visitLogicalExpr(self, expr: LogicalExpr) -> Any:
        left: Any = self.eval(expr=expr.left)

        if expr.operator.type == TT.OR:
            if self.__bool_from_any(left):
                return left
        elif expr.operator.type == TT.AND:
            if not self.__bool_from_any(left):
                return left

        return self.eval(expr=expr.right)

    def visitBinaryExpr(self, expr: BinaryExpr) -> Any:
        left: Any = self.eval(expr.left)
        right: Any = self.eval(expr.right)

        match expr.operator.type:
            case TT.MINUS:
                self.__check_num_bin_operand(
                    op=expr.operator, left=left, right=right
                )
                return float(left) - float(right)
            case TT.SLASH:
                self.__check_num_bin_operand(
                    op=expr.operator, left=left, right=right
                )
                return float(left) / float(right)
            case TT.STAR:
                self.__check_num_bin_operand(
                    op=expr.operator, left=left, right=right
                )
                return float(left) * float(right)
            case TT.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)

                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

                raise RuntimeException(
                    expr.operator,
                    "Operands must be two numbers or two strings.",
                )
            case TT.GT:
                self.__check_num_bin_operand(
                    op=expr.operator, left=left, right=right
                )
                return float(left) > float(right)
            case TT.GTE:
                self.__check_num_bin_operand(
                    op=expr.operator, left=left, right=right
                )
                return float(left) >= float(right)
            case TT.LT:
                self.__check_num_bin_operand(
                    op=expr.operator, left=left, right=right
                )
                return float(left) < float(right)
            case TT.LTE:
                self.__check_num_bin_operand(
                    op=expr.operator, left=left, right=right
                )
                return float(left) <= float(right)
            case TT.EQ_EQ:
                return self.__is_eq(left, right)
            case TT.BANG_EQ:
                return not self.__is_eq(left, right)

        return None

    def visitVariableExpr(self, expr: VariableExpr) -> Any:
        return self.ctx.get(expr.name)

    # StmtVisitor

    def visitExpressionStmt(self, stmt: ExpressionStmt) -> None:
        self.eval(stmt.expression)
        return None

    def visitIfStmt(self, stmt: IfStmt) -> None:
        if self.__bool_from_any(self.eval(stmt.condition)):
            return self.execute(stmt.thenBranch)
        elif stmt.elseBranch != ExpressionStmt(LiteralExpr(None)):
            return self.execute(stmt.elseBranch)

    def visitWhileStmt(self, stmt: WhileStmt) -> None:
        while self.__bool_from_any(self.eval(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visitPrintStmt(self, stmt: PrintStmt) -> None:
        value: Any = self.eval(stmt.expression)
        print(self.stringify(value))
        return None

    def visitVarStmt(self, stmt: VarStmt) -> None:
        value: Any = None
        if stmt.initializer is not None:
            value = self.eval(stmt.initializer)

        self.ctx.define(stmt.name.lexeme, value)
        return None

    def visitBlockStmt(self, stmt: BlockStmt) -> None:
        self.__exec_block(stmt.statements)
        return None

    def __exec_block(self, stmts: list[Stmt]) -> None:
        self.ctx.parent = copy.deepcopy(self.ctx)
        self.ctx.values = {}

        for stmt in stmts:
            self.execute(stmt)
        self.ctx.values = self.ctx.parent.values
        self.ctx.parent = self.ctx.parent.parent

    def __bool_from_any(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return bool(value)

        return True

    def __is_eq(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True

        if a is None:
            return False

        return a == b

    def stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            text: str = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)

    # Runtime errors

    def __check_num_un_operand(self, op: Token, right: Any):
        if not isinstance(right, float):
            raise RuntimeException(op, "operand must be a number.")

    def __check_num_bin_operand(self, op: Token, left: Any, right: Any):
        if not isinstance(right, float) or not isinstance(left, float):
            raise RuntimeException(op, "operands must be numbers.")
