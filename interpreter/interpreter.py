from .token import TokenType
from .lexer import Lexer


class Interpreter:

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token = self.lexer.get_next_token()

    def eat(self, token_type: TokenType):
        if self.token.type_ == token_type:
            self.token = self.lexer.get_next_token()
        else:
            self.lexer.error()

    def factor(self) -> int:
        t = self.token
        self.eat(TokenType.INTEGER)
        return t.val

    def term(self) -> int:
        res = self.factor()
        while self.token.type_ in (TokenType.MUL, TokenType.DIV):
            oper = self.token.val
            self.eat(self.lexer.operation_types[oper])
            res = self.lexer.operations[oper](res, self.factor())
        return res

    def expr(self) -> int:
        res = self.term()
        while self.token.type_ in (TokenType.PLUS, TokenType.MINUS):
            oper = self.token.val
            self.eat(self.lexer.operation_types[oper])
            res = self.lexer.operations[oper](res, self.term())
        return res

