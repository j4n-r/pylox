from __future__ import annotations

import sys

from scanner import Scanner


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
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)
        if Lox.hadError:
            exit(65)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Lox.hadError = True

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)


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
