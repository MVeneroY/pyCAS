import unittest
from cas.parser import get_token_type, TokenType
from cas.parser import str_to_tokens

class TestsParserMethods(unittest.TestCase):

    def test_get_token_type(self):
        self.assertEqual(
            get_token_type('x'),
            TokenType.Symbol
        )
        self.assertIsNone(
            get_token_type('xy')
        )
        self.assertEqual(
            get_token_type('1'),
            TokenType.Number
        )
        self.assertIsNone(
            get_token_type('-1')
        )

    def test_str_to_tokens(self):
        self.assertListEqual(
            str_to_tokens("-2"),
            ['-', '2']
        )
        self.assertListEqual(
            str_to_tokens("3x+4"),
            ['3', 'x', '+', '4']
        )


if __name__ == '__main__':
    unittest.main()