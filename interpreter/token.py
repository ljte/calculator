from typing import Any
from enum import Enum


class TokenType(Enum):
    EOF = 0
    INTEGER = 1
    PLUS = 2
    MINUS = 3
    MUL = 4
    DIV = 5
    OPAREN = 6  # opening parenthesis
    CPAREN = 7  # closing parenthesis


class Token:

    def __init__(self, val: Any, type_: TokenType):
        self.val = val
        self.type_ = type_

    def __repr__(self):
        return f"{self.__class__.__name__}({self.val}, {self.type_})"

    def __eq__(self, other):
        return self.val == other.val and self.type_ == other.type_
