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
        if t.type_ == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return t.val
        elif t.type_ == TokenType.OPAREN:
            self.eat(TokenType.OPAREN)
            r = self.expr()
            self.eat(TokenType.CPAREN)
            return r

    def term(self) -> int:
        res = self.factor()
        while self.token.type_ in (TokenType.MUL, TokenType.DIV):
            oper = self.token.val
            self.eat(self.lexer.token_types_mapping[oper])
            res = self.lexer.token_values_mapping[oper](res, self.factor())
        return res

    def expr(self) -> int:
        res = self.term()
        while self.token.type_ in (TokenType.PLUS, TokenType.MINUS):
            oper = self.token.val
            self.eat(self.lexer.token_types_mapping[oper])
            res = self.lexer.token_values_mapping[oper](res, self.term())
        return res

