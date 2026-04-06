import unittest
from cas import Expression
from cas.engine import substitute, evaluate

class TestEngineMethods(unittest.TestCase):
    
    def test_substitute(self):
        s = Expression('3x+4')
        s2 = substitute(s, 'x', 8)
        self.assertEqual(
            s2.__repr__(),
            'Add( Mul( 3, 8 ), 4 )'
        )

    def test_evaluate(self):
        self.assertEqual(
            evaluate(Expression('3^2 + 16*5 +4')),
            93
        )


if __name__ == '__main__':
    unittest.main()