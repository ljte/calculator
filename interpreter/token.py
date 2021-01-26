from typing import Any
from enum import Enum, auto


class TokenType(Enum):
    EOF = auto()
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    OPAREN = auto()  # opening parenthesiauto()
    CPAREN = auto()  # closing parenthesiauto(auto()


class Token:

    def __init__(self, val: Any, type_: TokenType):
        self.val = val
        self.type_ = type_

    def __repr__(self):
        return f"{self.__class__.__name__}({self.val}, {self.type_})"

    def __eq__(self, other):
        return self.val == other.val and self.type_ == other.type_
