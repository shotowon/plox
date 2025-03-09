from pathlib import Path
from sys import stderr
import io

from plox.backend.visitors.eval import Eval, RuntimeException, Context
from plox.frontend.parser import ParseException, Parser
from plox.frontend.scanner import Scanner
from plox.frontend.tokens import Token, TokenType


class Interpreter:
    def __init__(self):
        self.errors: list[str] = []
        self.ctx = Context()
        self.had_errors: bool = False

    def run_interactively(self) -> None:
        src = io.StringIO()
        print("Enter '\\quit' to exit. ^.^")
        print("Enter '\\clean' to clean buffered lines. 0.0")
        print("Enter '\\lines' to print buffered lines. -_-")
        print("Enter '\\errors' to print syntactical errors. @~@")
        while True:
            try:
                line = input("> ")
                if line.strip() == "":
                    continue
                if line.strip() == "\\quit":
                    for err in self.errors:
                        stderr.write(err)
                    src.seek(0)
                    src.truncate()
                    self.errors = []
                    break
                if line.strip() == "\\clean":
                    for err in self.errors:
                        stderr.write(err)
                    src.seek(0)
                    src.truncate()
                    self.errors = []
                    continue
                if line.strip() == "\\lines":
                    print(src.getvalue())
                    continue
                if line.strip() == "\\errors":
                    for err in self.errors:
                        stderr.write(err)
                    continue
                src.write(line)

                scanner: Scanner = Scanner(source=src.getvalue())
                tokens: list[Token] = []
                for token in scanner:
                    if token.type == TokenType.INVALID:
                        self.__error(token, token.meta)
                        continue
                    tokens.append(token)

                parser: Parser = Parser(tokens=tokens)
                stmts = parser.parse()
                if len(parser.errors) != 0:
                    self.errors = []
                    for err in parser.errors:
                        self.__error(token=err.token, message=err.message)
                    src.write("\n")
                    continue

                try:
                    eval: Eval = Eval(self.ctx)
                    for stmt in stmts:
                        eval.execute(stmt=stmt)
                except RuntimeException as e:
                    self.__report(
                        line=e.token.line,
                        where=f"at '{e.token.lexeme}'",
                        message=e.message,
                    )
                    for err in self.errors:
                        stderr.write(err)
                finally:
                    src.seek(0)
                    src.truncate()
                    self.errors = []
            except EOFError:
                print("\nEnd of input. Exiting...")
                break
            except KeyboardInterrupt:
                print("\nInput interrupted. Exiting...")
                break
        if self.had_errors:
            exit(65)

    def run_file(self, filepath: Path) -> None:
        try:
            with open(filepath, "r") as f:
                text: str = f.read()

            self.__run(text)
            if len(self.errors) != 0:
                for err in self.errors:
                    stderr.write(err)
                exit(65)
        except FileNotFoundError as e:
            stderr.write(f"file: {filepath.name} not found: {e}")
        except IOError as e:
            stderr.write(f"I/O error: {e}")
        except Exception as e:
            stderr.write(f"unexpected error occured: {e}")

    def __run(self, source: str) -> None:
        scanner: Scanner = Scanner(source=source)
        tokens: list[Token] = []
        for token in scanner:
            if token.type == TokenType.INVALID:
                self.__error(token, token.meta)
                continue
            tokens.append(token)

        parser: Parser = Parser(tokens=tokens)
        stmts = parser.parse()
        if len(parser.errors) != 0:
            for err in parser.errors:
                self.__error(token=err.token, message=err.message)
            for err in self.errors:
                stderr.write(err)
            return

        eval: Eval = Eval(self.ctx)
        try:
            for stmt in stmts:
                eval.execute(stmt=stmt)
        except RuntimeException as e:
            self.__report(
                line=e.token.line,
                where=f"at '{e.token.lexeme}'",
                message=e.message,
            )

    def __error(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            return self.__report(
                line=token.line,
                where="at end",
                message=message,
            )

        return self.__report(
            line=token.line,
            where=f"at '{token.lexeme}'",
            message=message,
        )

    def __report(self, line: int, where: str, message: str) -> None:
        self.errors.append(f"[line {line}] Error {where}: {message}\n")
