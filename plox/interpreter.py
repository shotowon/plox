from pathlib import Path

from plox.backend.visitors.pprint import PPrintVisitor
from plox.frontend.parser import ParseException, Parser
from plox.frontend.scanner import Scanner
from plox.frontend.tokens import Token, TokenType


class Interpreter:
    def __init__(self):
        self.errors: list[str] = []

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
                        print(err)
            except EOFError:
                print("\nEnd of input. Exiting...")
                break
            except KeyboardInterrupt:
                print("\nInput interrupted. Exiting...")
                break

    def run_file(self, filepath: Path) -> None:
        try:
            with open(filepath, "r") as f:
                text: str = f.read()

            self.__run(text)
            if len(self.errors) != 0:
                for err in self.errors:
                    print(err)
                exit(65)
        except FileNotFoundError as e:
            print(f"file: {filepath.name} not found: {e}")
        except IOError as e:
            print(f"I/O error: {e}")
        except Exception as e:
            print(f"unexpected error occured: {e}")

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
            expr = parser.parse()
        except ParseException as e:
            self.__error(token=e.token, message=e.message)
            for err in self.errors:
                print(err)
            return

        pprinter: PPrintVisitor = PPrintVisitor()
        pprinter.print(expr=expr)

    def __error(self, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            return self.__report(
                line=token.line,
                where="at end",
                message=message,
            )

        return self.__report(
            line=token.line,
            where=f"at '{token.lexeme}",
            message=message,
        )

    def __report(self, line: int, where: str, message: str) -> None:
        self.errors.append(f"[line {line}] Error {where}: {message}")
