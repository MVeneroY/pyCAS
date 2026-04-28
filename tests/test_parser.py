import unittest
from cas.lexer import gettokens
from cas.parser import _parsetokens, _parse_term, _parse_factor


class TestLexerMethods(unittest.TestCase):
    def test_parsetokens(self):
        self.assertEqual(
            _parsetokens(gettokens("-1+4")).tostring(),
            "+ ( * ( -1, 1 ), 4 )",
        )
        self.assertEqual(
            _parsetokens(gettokens("3*x + 4")).tostring(),
            "+ ( * ( 3, x ), 4 )",
        )
        self.assertEqual(
            _parsetokens(gettokens("3 + x + y + 2x")).tostring(),
            "+ ( 3, x, y, * ( 2, x ) )",
        )
        self.assertEqual(
            _parsetokens(gettokens("-2 / -2 - 2")).tostring(),
            "+ ( * ( -1, * ( 2, ^ ( * ( -1, 2 ), -1 ) ) ), * ( -1, 2 ) )",
        )
        self.assertEqual(
            _parsetokens(gettokens("3x^2 + 2")).tostring(),
            "+ ( * ( 3, ^ ( x, 2 ) ), 2 )",
        )

    def test_gen_term(self):
        self.assertEqual(
            _parse_term(gettokens("2*x")).tostring(), 
            "* ( 2, x )"
        )
        self.assertEqual(
            _parse_term(gettokens("2/x")).tostring(), 
            "* ( 2, ^ ( x, -1 ) )"
        )
        self.assertEqual(
            _parse_term(gettokens("2*x*3")).tostring(),
            "* ( 2, x, 3 )",
        )
        self.assertEqual(
            _parse_term(gettokens("-2 * x")).tostring(),
            "* ( * ( -1, 2 ), x )",
        )
        self.assertEqual(
            _parse_term(gettokens("x * -2")).tostring(),
            "* ( x, * ( -1, 2 ) )",
        )

    def test_parse_factor(self):
        self.assertEqual(
            _parse_factor(gettokens("2")).tostring(),
            "2",
        )
        self.assertEqual(
            _parse_factor(gettokens("x**3")).tostring(),
            "^ ( x, 3 )",
        )
        self.assertEqual(
            _parse_factor(gettokens("3xy")).tostring(), 
            "* ( 3, x, y )"
        )
        self.assertEqual(
            _parse_factor(gettokens("2cos(x)^8z")).tostring(),
            "* ( 2, ^ ( cos ( x ), 8 ), z )",
        )


if __name__ == "__main__":
    unittest.main()
