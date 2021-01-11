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

    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"

    def __str__(self):
        return self.__repr__()


class Interpreter:

    oper_types = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.ASTRISK,
        '/': TokenType.SLASH,
    }

    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
    }

    def __init__(self, text):
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

    def get_next_token(self):
        while self.current_ch:

            if self.current_ch.isspace():
                self.skip_whitespaces()
                continue

            if self.current_ch.isdigit():
                return Token(TokenType.INTEGER, self.extract_number())

    #        if self.current_ch == '-':
    #            self.advance()
    #            return Token(TokenType.MINUS, '-')
#
#            if self.current_ch == '+':
#                self.advance()
#                return Token(TokenType.PLUS, '+')
#
#            if self.current_ch == '*':
#                self.advance()
#                return Token(TokenType.ASTRISK, '*')
##
#            if self.current_ch == '/':
#                self.advance()
#                return Token(TokenType.SLASH, '/')

            if self.current_ch in ['+', '-', '*', '/']:
                self.advance()
                return Token(self.oper_types[self.current_ch], self.current_ch)

            self.error()

        return Token(TokenType.EOF, None)

    def error(self):
        raise Exception(f"Error parsing input")
        
    def eat(self, token_type):
        if self.token.type_ == token_type:
            self.token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.token = self.get_next_token()
        
        left = self.token
        self.eat(TokenType.INTEGER)

        oper = self.token
        if oper.type_ == TokenType.MINUS:
            self.eat(TokenType.MINUS)
        elif oper.type_ == TokenType.PLUS:
            self.eat(TokenType.PLUS) 
        elif oper.type_ == TokenType.ASTRISK:
            self.eat(TokenType.ASTRISK)
        elif oper.type_ == TokenType.SLASH:
            self.eat(TokenType.SLASH)

        right = self.token
        self.eat(TokenType.INTEGER)

        if oper.type_ == TokenType.MINUS:
            return left.value - right.value
        elif oper.type_ == TokenType.PLUS:
            return left.value + right.value
        elif oper.type_ == TokenType.ASTRISK:
            return left.value * right.value
        elif oper.type_ == TokenType.SLASH:
            return left.value / right.value

    def extract_number(self):
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
        except (KeyboardInterrupt, EOFError):
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        print(interpreter.expr())

