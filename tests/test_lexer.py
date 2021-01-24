import unittest

from interpreter import Lexer, Token, TokenType


class TestLexer(unittest.TestCase):

    def test_advance(self):
        l = Lexer('42 2')
        l.advance()
        assert l.pos == 1
        assert l.text[l.pos] == '2'

    def test_skip_whitespaces(self):
        l = Lexer('   43')
        l.skip_whitespaces()
        assert l.pos == 3

    def test_extract_number(self):
        l = Lexer('12 43')
        assert l.extract_number() == 12
        l.skip_whitespaces()
        assert l.extract_number() == 43

    def test_get_next_token(sefl):
        l = Lexer('20 + 24')

        assert l.get_next_token() == Token(20, TokenType.INTEGER)
        assert l.get_next_token() == Token('+', TokenType.PLUS)
        assert l.get_next_token() == Token(24, TokenType.INTEGER)


if __name__ == '__main__':
    unittest.main()
