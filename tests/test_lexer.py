import unittest
from cas.parser import str_to_tokens
from cas.lexer import _generate_factor as generate_factor
from cas.lexer import _generate_term as generate_term
from cas.lexer import _generate_expr as generate_expr

class TestLexerMethods(unittest.TestCase):

    def test_gen_factor(self):
        self.assertEqual(
            generate_factor(str_to_tokens('-2')).ops_to_string(),
            'Mul( -1, 2 )'
        )
        self.assertEqual(
            generate_factor(str_to_tokens('x ^ 7')).ops_to_string(),
            'Pow( x, 7 )'
        )
        self.assertEqual(
            generate_factor(str_to_tokens('-x**3')).ops_to_string(),
            'Mul( -1, Pow( x, 3 ) )'
        )
        self.assertEqual(
            generate_factor(str_to_tokens('2^x')).ops_to_string(),
            'Pow( 2, x )'
        )
        self.assertEqual(
            generate_factor(str_to_tokens('1')).ops_to_string(),
            '1'
        )
        self.assertEqual(
            generate_factor(str_to_tokens('y')).ops_to_string(),
            'y'
        )
        
    def test_gen_term(self):
        self.assertEqual(
            generate_term(str_to_tokens('2*x')).ops_to_string(),
            'Mul( 2, x )'
        )
        self.assertEqual(
            generate_term(str_to_tokens('2/x')).ops_to_string(),
            'Div( 2, x )'
        )
        self.assertEqual(
            generate_term(str_to_tokens('2*x*3')).ops_to_string(),
            'Mul( Mul( 2, x ), 3 )'
        )
        self.assertEqual(
            generate_term(str_to_tokens('-2 * x')).ops_to_string(),
            'Mul( Mul( -1, 2 ), x )'
        )
        self.assertEqual(
            generate_term(str_to_tokens('x * -2')).ops_to_string(),
            'Mul( x, Mul( -1, 2 ) )'
        )

    def test_gen_expr(self):
        self.assertEqual(
            generate_expr(str_to_tokens('3*x + 4')).ops_to_string(),
            'Add( Mul( 3, x ), 4 )'
        )
        self.assertEqual(
            generate_expr(str_to_tokens('3 + x')).ops_to_string(),
            'Add( 3, x )'
        )
        self.assertEqual(
            generate_expr(str_to_tokens('-2 / -2 - 2')).ops_to_string(),
            'Sub( Div( Mul( -1, 2 ), Mul( -1, 2 ) ), 2 )'
        )
        self.assertEqual(
            generate_expr(str_to_tokens('3x^2 + 2')).ops_to_string(),
            'Add( Mul( 3, Pow( x, 2 ) ), 2 )'
        )

if __name__ == '__main__':
    unittest.main()