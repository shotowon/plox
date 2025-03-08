from pathlib import Path
from typing import Any
from sys import stderr

from plox.backend.visitors.eval import Eval, RuntimeException
from plox.frontend.parser import ParseException, Parser
from plox.frontend.scanner import Scanner
from plox.frontend.tokens import Token, TokenType


class Interpreter:
    def __init__(self):
        self.errors: list[str] = []
        self.had_errors: bool = False

    def run_interactively(self) -> None:
        print("Enter 'quit' to exit. ^.^")
        while True:
            self.errors = []
            try:
                line: str = input("> ")
                if line.strip() == "":
                    continue
                if line.strip() == "quit":
                    break
                self.__run(line)

                if len(self.errors) != 0:
                    for err in self.errors:
                        self.had_errors = True
                        stderr.write(err)
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
        try:
            stmts = parser.parse()
        except ParseException as e:
            self.__error(token=e.token, message=e.message)
            for err in self.errors:
                stderr.write(err)
            return

        eval: Eval = Eval()
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
