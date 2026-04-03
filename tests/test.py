import unittest
from cas import parser
from cas import lexer

class TestNodeMethods(unittest.TestCase):

    def test_str_to_tokens1(self):
        self.assertEqual(
            parser.str_to_tokens("-2"),
            ['-', '2']
        )

    def test_str_to_tokens2(self):
        self.assertEqual(
            parser.str_to_tokens("3x+4"),
            ['3', 'x', '+', '4']
        )

    def test_gen_factor1(self):
        self.assertEqual(
            lexer.generate_factor(parser.str_to_tokens('-2')).ops_to_string(),
                           'Mul( -1, 2 )')
        
    def test_gen_factor2(self):
        self.assertEqual(
            lexer.generate_factor(parser.str_to_tokens('x ^ 7')).ops_to_string(),
                           'Pow( x, 7 )')
        
    def test_gen_factor3(self):
        self.assertEqual(
            lexer.generate_factor(parser.str_to_tokens('-x**3')).ops_to_string(),
                           'Mul( -1, Pow( x, 3 ) )')

    def test_gen_factor4(self):
        self.assertEqual(
            lexer.generate_factor(parser.str_to_tokens('2^x')).ops_to_string(),
                           'Pow( 2, x )')

if __name__ == '__main__':
    unittest.main()