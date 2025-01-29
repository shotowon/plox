from pathlib import Path
import sys

from interpreter import Interpreter


def main():
    match len(sys.argv):
        case 2:
            interpreter: Interpreter = Interpreter()
            interpreter.run_file(Path(sys.argv[1]))
        case 1:
            interpreter: Interpreter = Interpreter()
            interpreter.run_interactively()
        case _:
            print(f"usage: {sys.argv[0]} <file_path>")
            print(f"or just '{sys.argv[0]}' to run in interactive mode")
            exit(64)


if __name__ == "__main__":
    main()
