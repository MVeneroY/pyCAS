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
        
    def test_gen_factor5(self):
        self.assertEqual(
            lexer.generate_factor(parser.str_to_tokens('1')).ops_to_string(),
                           '1')
        
    def test_gen_factor6(self):
        self.assertEqual(
            lexer.generate_factor(parser.str_to_tokens('y')).ops_to_string(),
                           'y')
        
    def test_gen_term1(self):
        self.assertEqual(
            lexer.generate_term(parser.str_to_tokens('2*x')).ops_to_string(),
                            'Mul( 2, x )'
        )

    def test_gen_term2(self):
        self.assertEqual(
            lexer.generate_term(parser.str_to_tokens('2/x')).ops_to_string(),
                            'Div( 2, x )'
        )

    def test_gen_term3(self):
        self.assertEqual(
            lexer.generate_term(parser.str_to_tokens('2*x*3')).ops_to_string(),
                            'Mul( Mul( 2, x ), 3 )'
        )

    def test_gen_term4(self):
        self.assertEqual(
            lexer.generate_term(parser.str_to_tokens('-2 * x')).ops_to_string(),
                            'Mul( Mul( -1, 2 ), x )'
        )

    def test_gen_term5(self):
        self.assertEqual(
            lexer.generate_term(parser.str_to_tokens('x * -2')).ops_to_string(),
                            'Mul( x, Mul( -1, 2 ) )'
        )

    def test_gen_expr1(self):
        self.assertEqual(
            lexer.generate_expr(parser.str_to_tokens('3*x + 4')).ops_to_string(),
                            'Add( Mul( 3, x ), 4 )'
        )

    def test_gen_expr2(self):
        self.assertEqual(
            lexer.generate_expr(parser.str_to_tokens('3 + x')).ops_to_string(),
                            'Add( 3, x )'
        )

    def test_gen_expr3(self):
        self.assertEqual(
            lexer.generate_expr(parser.str_to_tokens('-2 / -2 - 2')).ops_to_string(),
                            'Sub( Div( Mul( -1, 2 ), Mul( -1, 2 ) ), 2 )'
        )

if __name__ == '__main__':
    unittest.main()