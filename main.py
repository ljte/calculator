from typing import Dict, Callable, Any
from enum import Enum
import operator


class TokenType(Enum):
    EOF = 0
    PLUS = 1
    MINUS = 2
    INTEGER = 3
    ASTRISK = 4
    SLASH = 5


class Token:

    def __init__(self, type_: TokenType, value: Any):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"

    def __str__(self):
        return self.__repr__()


class Interpreter:

    oper_types: Dict[str, TokenType] = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.ASTRISK,
        '/': TokenType.SLASH,
    }

    operations: Dict[str, Callable] = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
    }

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.token = None
        self.current_ch = self.text[self.pos]

    def skip_whitespaces(self):
        while self.text[self.pos].isspace():
            self.advance()

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_ch = None
        else:
            self.current_ch = self.text[self.pos]

    def get_next_token(self) -> Token:
        while self.current_ch:

            if self.current_ch.isspace():
                self.skip_whitespaces()
                continue

            if self.current_ch.isdigit():
                return Token(TokenType.INTEGER, self.extract_number())

            if self.current_ch in self.operations:
                ch = self.current_ch
                self.advance()
                return Token(self.oper_types[ch], ch)

            self.error()

        return Token(TokenType.EOF, None)

    def error(self):
        raise Exception(f"Error parsing input")
        
    def eat(self, token_type):
        if self.token.type_ == token_type:
            self.token = self.get_next_token()
        else:
            self.error()

    def term(self) -> int:
        t = self.token
        self.eat(TokenType.INTEGER)
        return t.value

    def expr(self) -> int:
        if self.text == "quit()":
            raise EOFError

        self.token = self.get_next_token()
        result = self.term()

        while self.current_ch:
            oper = self.token.value
            self.eat(self.oper_types[oper])
            result = self.operations[oper](result, self.term())
           
        return result

    def extract_number(self) -> int:
        res = ''
        try:
            while self.current_ch.isdigit():
                res += self.current_ch
                self.advance()
        except AttributeError:
            pass
        return int(res)


if __name__ == "__main__":

    while True:
        try:
            text = input(">>> ")

            if not text:
                continue

            interpreter = Interpreter(text)
            print(interpreter.expr())
        except (KeyboardInterrupt, EOFError):
            break


