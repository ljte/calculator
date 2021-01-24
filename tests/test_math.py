import unittest

from interpreter import Interpreter, Lexer, Token, TokenType


class TestMath(unittest.TestCase):

    def test_eat(self):
        inter = Interpreter(Lexer('12 + 23'))

        assert inter.token == Token(12, TokenType.INTEGER)
        inter.eat(TokenType.INTEGER)

        assert inter.token == Token('+', TokenType.PLUS)
        inter.eat(TokenType.PLUS)

        assert inter.token == Token(23, TokenType.INTEGER)

    def test_error_eat(self):
        inter = Interpreter(Lexer('+ 23'))

        with self.assertRaises(Exception):
            inter.eat(TokenType.INTEGER)

    def test_factor(self):
        inter = Interpreter(Lexer('25 * 12 + 23'))

        assert inter.token.val == 25

        inter.eat(TokenType.INTEGER)
        inter.eat(TokenType.MUL)

        assert inter.factor() == 12

        inter.eat(TokenType.PLUS)

        assert inter.factor() == 23

    def test_term(self):
        inter = Interpreter(Lexer('2 * 5 * 14 / 2 * 4'))
        assert inter.term() == 280

    def text_expr(self):
        inter = Interpreter(Lexer('4 + 5 * 3 - 72 / 36 * 4'))
        assert inter.expr() == 11


if __name__ == '__main__':
    unittest.main()


