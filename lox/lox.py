from __future__ import annotations

import sys

from .ast_printer import AstPrinter
from .scanner import Scanner
from .token_type import Token, TokenType


class Lox:
    hadError = False

    @staticmethod
    def run_file(path: str):
        with open(path, "r") as file:
            Lox.run(file.read())

    @staticmethod
    def run_prompt():
        while True:
            line = input("> ")
            if line == "":
                break
            Lox.run(line)
            Lox.hadError = False

    @staticmethod
    def run(source: str):
        from .parser import Parser

        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        print(tokens)
        parser = Parser(tokens)
        expression = parser.parse()

        if Lox.hadError:
            return

        # Add this null check:
        if expression is None:
            print("Failed to parse expression")
            return
        print(AstPrinter().print(expression))

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Lox.hadError = True

    @staticmethod
    def error(token: Token, message: str):
        if token.type is TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)


def main():
    lox = Lox()
    if len(sys.argv) < 1:
        print("Usage: plox [script]")
        exit()
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
