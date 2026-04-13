import unittest
from cas.lexer import Token, TokenType
from cas.lexer import str_to_tokens

class TestsParserMethods(unittest.TestCase):

    def test_get_token_type(self):
        self.assertEqual(
            Token.get_token_type('x'),
            TokenType.Symbol
        )
        self.assertIsNone(
            Token.get_token_type('xy')
        )
        self.assertEqual(
            Token.get_token_type('1'),
            TokenType.Number
        )
        self.assertIsNone(
            Token.get_token_type('-1')
        )

    def test_str_to_tokens(self):
        self.assertListEqual(
            [t.literal() for t in str_to_tokens("-2")],
            ['-', '2']
        )
        self.assertListEqual(
            [t.literal() for t in str_to_tokens("3x+4")],
            ['3', 'x', '+', '4']
        )
        self.assertListEqual(
            [t.literal() for t in str_to_tokens("2x**2-3.6x+3")],
            ['2', 'x', '^', '2', '-', '3.6', 'x', '+', '3']
        )


if __name__ == '__main__':
    unittest.main()