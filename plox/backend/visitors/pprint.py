import io

from plox.frontend.ast import (
    Expr,
    ExprVisitor,
    BinaryExpr,
    GroupingExpr,
    LiteralExpr,
    UnaryExpr,
)


class PPrintVisitor(ExprVisitor[str]):
    def print(self, expr: Expr) -> None:
        print(expr.accept(visitor=self))

    def visitBinaryExpr(self, expr: BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: GroupingExpr) -> str:
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: UnaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        buf = io.StringIO()
        buf.write("(")
        buf.write(name)
        for expr in exprs:
            buf.write(f" {expr.accept(self)}")
        buf.write(")")

        return buf.getvalue()
