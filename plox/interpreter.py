from typing import List
from pathlib import Path

from plox.scanner import Scanner


class Interpreter:
    def __init__(self):
        self.errors: List[str] = []

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
                        exit(65)
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
            print(f"I/O error occured: {e}")
        except Exception as e:
            print(f"unexpected error occured: {e}")

    def __run(self, source: str) -> None:
        scanner: Scanner = Scanner(source=source)
        tokens = [token for token in scanner]
        print(tokens)

    def __error(self, line: int, message: str) -> None:
        self.__report(line=line, where="", message=message)

    def __report(self, line: int, where: str, message: str) -> None:
        self.errors.append(f"[line {line}] Error{where}: {message}")
