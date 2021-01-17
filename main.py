from typing import Dict, Callable, Any
from enum import Enum
import operator


class TokenType(Enum):
    EOF = 0
    PLUS = 1
    MINUS = 2
    INTEGER = 3
    MUL = 4
    DIV = 5


class Token:

    def __init__(self, type_: TokenType, value: Any):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"

    def __str__(self):
        return self.__repr__()


class Lexer:

    oper_types: Dict[str, TokenType] = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MUL,
        '/': TokenType.DIV,
    }

    operations: Dict[str, Callable] = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
    }
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_ch = text[self.pos]

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

    def extract_number(self) -> int:
        res = ''
        try:
            while self.current_ch.isdigit():
                res += self.current_ch
                self.advance()
        except AttributeError:
            pass
        return int(res)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text})"


class Interpreter:

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token = self.lexer.get_next_token()
        
    def eat(self, token_type):
        if self.token.type_ == token_type:
            self.token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self) -> int:
        t = self.token
        self.eat(TokenType.INTEGER)
        return t.value

    def term(self) -> int:
        res = self.factor()

        while self.token.type_ in (TokenType.MUL, TokenType.DIV):
            oper = self.token.value
            self.eat(self.lexer.oper_types[oper])
            res = self.lexer.operations[oper](res, self.factor())
        
        return res

    def expr(self) -> int:
        res = self.term()

        while self.token.type_ in (TokenType.PLUS, TokenType.MINUS):
            oper = self.token.value
            self.eat(self.lexer.oper_types[oper])
            res = self.lexer.operations[oper](res, self.term())
           
        return res
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.lexer})"


if __name__ == "__main__":
    
    while True:
        try:
            text = input(">>> ")

            if not text:
                continue

            r = Interpreter(Lexer(text)).expr()
            print(r)
        except (KeyboardInterrupt, EOFError):
            break


