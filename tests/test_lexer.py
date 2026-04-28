import unittest
from cas.lexer import gettokens

class TestsParserMethods(unittest.TestCase):
 
    def test_str_to_tokens(self):
        self.assertListEqual(
            [t.literal() for t in gettokens("-2")], 
            ["-", "2"]
        )
        self.assertListEqual(
            [t.literal() for t in gettokens("3x+4")], ["3", "x", "+", "4"]
        )
        self.assertListEqual(
            [t.literal() for t in gettokens("2x**2-3.6x+3")],
            ["2", "x", "^", "2", "-", "3.6", "x", "+", "3"],
        )
        self.assertListEqual(
            [t.literal() for t in gettokens("cos(sin(tan(xy)))")],
            ["cos", "(", "sin", "(", "tan", "(", "x", "y", ")", ")", ")"]            
        )


if __name__ == "__main__":
    unittest.main()
