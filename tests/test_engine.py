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
        s = Expression('25x**2 - y**2')
        s2 = substitute(s, 'x', '0.7')
        self.assertEqual(
            s2.__repr__(),
            'Sub( Mul( 25, Pow( 0.7, 2 ) ), Pow( y, 2 ) )'
        )

    def test_evaluate(self):
        self.assertEqual(
            evaluate(Expression('3^2 + 16*5 +4')),
            93
        )
        self.assertAlmostEqual(
            evaluate(Expression('32 + 16*5 +4/3')),
            113.33333333
        )


if __name__ == '__main__':
    unittest.main()