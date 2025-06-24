from token import Token, TokenType
from typing import Final


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str):
        self.source = source
        self.tokens: Final[list] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def addToken(self, type_: TokenType, literal: object = None):
        text = str = self.source[self.start : self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

    def match(self, expected: str):
        """
        Returns the equality of `expected` to `current` \n
        sets current += 1 if true
        """
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self) -> str:
        if self.current + 1 <= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1

        if self.isAtEnd():
            from lox import Lox

            Lox.error(self.line, "Unterminated String")
            return
        # the closing " from the string
        self.advance()
        value: str = self.source[self.start + 1 : self.current - 1]
        self.addToken(TokenType.STRING, value)

    def number(self):
        while self.peek().isnumeric():
            self.advance()
        if self.peek() == "." and self.peekNext().isnumeric():
            self.advance()
            while self.peek().isnumeric():
                self.advance()
        self.addToken(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()
        text: str = self.source[self.start : self.current]
        type_ = self.keywords.get(text)
        if type_ is None:
            type_ = TokenType.IDENTIFIER
        self.addToken(type_)

    def scanToken(self):
        c = self.advance()
        match c:
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            case "*":
                self.addToken(TokenType.STAR)
            case "!":
                self.addToken(
                    TokenType.BANG_EQUAL if self.match("!") else TokenType.BANG
                )
            case "=":
                self.addToken(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.addToken(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.addToken(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    # A comment goes until the end of the line.
                    while self.peek() != "\n" and not self.isAtEnd():
                        self.advance()
                elif self.match("*"):
                    while self.peek() != "*" and self.peekNext() != "/":
                        if self.isAtEnd():
                            self.line += 1
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            case " " | "\r" | "\t":  # ignore whitespace
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()

            case _:
                if c.isnumeric:
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    from lox import Lox

                    Lox.error(self.line, "Unexpected character.")
