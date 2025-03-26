from typing import Any, TYPE_CHECKING
from datetime import datetime
import time

from plox.backend.visitors.eval.runtime import LoxCallable

if TYPE_CHECKING:
    from plox.backend.visitors.eval.visitor import Eval


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, eval: "Eval", args: list[Any]) -> Any:
        return datetime.now().second


class Sleep(LoxCallable):
    def arity(self) -> int:
        return 1

    def call(self, eval: "Eval", args: list[Any]) -> Any:
        if len(args) != 1:
            raise RuntimeError("'sleep' expected seconds argument. Example: sleep(60).")
        seconds: float = args[0]
        if isinstance(seconds, float):
            time.sleep(seconds)
            return seconds
        raise RuntimeError(
            "'sleep' expected argument to be a number. Example: sleep(3.321)."
        )
