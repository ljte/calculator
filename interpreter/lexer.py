from typing import Dict, Callable, Any
import operator

from .token import TokenType, Token

class Lexer:

    token_values_mapping: Dict[str, Callable] = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
        '(': '(',
        ')': '(',
    }

    token_types_mapping: Dict[str, TokenType] = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MUL,
        '/': TokenType.DIV,
        '(': TokenType.OPAREN,
        ')': TokenType.CPAREN,
    }

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.curr_ch = text[self.pos]

    def skip_whitespaces(self):
        while self.curr_ch.isspace():
            self.advance()

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.curr_ch = None
        else:
            self.curr_ch = self.text[self.pos]

    def extract_number(self) -> int:
        res = ''
        try:
            while self.curr_ch.isdigit():
                res += self.curr_ch
                self.advance()
        except AttributeError:
            pass
        return int(res)

    def error(self):
        raise Exception("Error parsing input: %s" % self.text)

    def get_next_token(self) -> Token:
        while self.curr_ch:

            if self.curr_ch.isspace():
                self.skip_whitespaces()
                continue

            if self.curr_ch.isdigit():
                return Token(self.extract_number(), TokenType.INTEGER)

            if self.curr_ch in self.token_values_mapping:
                ch = self.curr_ch
                self.advance()
                return Token(ch, self.token_types_mapping[ch])

            self.error()

        return Token(None, TokenType.EOF)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.curr_ch})"

