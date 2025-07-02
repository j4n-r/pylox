from __future__ import annotations

import sys

from lox.errors import LoxRuntimeError
from lox.interpreter import Interpreter
from lox.scanner import Scanner
from lox.token_type import Token, TokenType


class Lox:
    interpreter = Interpreter()
    had_error = False
    had_runtime_error = False

    @staticmethod
    def run_file(path: str):
        with open(path, "r") as file:
            Lox.run(file.read())
        if Lox.had_error:
            exit(65)
        if Lox.had_runtime_error:
            exit(70)

    @staticmethod
    def run_prompt():
        while True:
            line = input("> ")
            if line == "":
                break
            Lox.run(line)
            Lox.had_error = False

    @staticmethod
    def run(source: str):
        from .parser import Parser

        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        statements = parser.parse()

        if Lox.had_error:
            return

        Lox.interpreter.interpret(statements)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True

    @staticmethod
    def error(token: Token, message: str):
        if token.type is TokenType.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error: LoxRuntimeError):
        print(f"{error} \n [line: {error.token.line}]", file=sys.stderr)
        Lox.had_runtime_error = True


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
