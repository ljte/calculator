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

    def expr(self):
        if self.text == "quit()":
            raise EOFError

        self.token = self.get_next_token()
        
        result = i = 0
        while self.current_ch:

            if i == 0:
                left = self.token
                self.eat(TokenType.INTEGER)
            else:
                left = Token(TokenType.INTEGER, result)

            oper = self.token
            self.eat(self.oper_types[oper.value])

            right = self.token
            self.eat(TokenType.INTEGER)
            
            result = self.operations[oper.value](left.value, right.value)
            i += 1
           
        return result

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

            if not text:
                continue

            interpreter = Interpreter(text)
            print(interpreter.expr())
        except (KeyboardInterrupt, EOFError):
            break


