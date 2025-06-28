from .token_type import Token


class LoxRuntimeError(Exception):
    token: Token

    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token
