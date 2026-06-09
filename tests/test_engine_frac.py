import unittest
from cas.ast_node import ASTNode
from cas.engine import frac
from cas.expression import Expression

class TestFracMethods(unittest.TestCase):
    def test_fromnum(self):
        num = ASTNode.number(3)
        f = frac.fromnum(num)

        self.assertEqual(
            f.tostring(),
            'frac ( 3, 1 )'
        )

    def test_add(self):
        f1 = ASTNode.frac(ASTNode.number(2), ASTNode.number(3))
        f2 = ASTNode.frac(ASTNode.number(5), ASTNode.number(7))

        self.assertEqual(
            frac.add(f1, f2).tostring(),
            'frac ( 29, 21 )'
        )

    def test_nadd(self):
        f = frac.nadd(
        ASTNode.frac(ASTNode.number(2), ASTNode.number(3)),
        ASTNode.frac(ASTNode.number(5), ASTNode.number(7)),
        ASTNode.frac(ASTNode.number(4), ASTNode.number(13)),
        ASTNode.frac(ASTNode.number(6), ASTNode.number(5))
        )

        self.assertEqual(
            f.tostring(),
            'frac ( 3943, 1365 )'
        )

    def test_sub(self):
        f1 = frac.fromints(3,7)
        f2 = frac.fromints(2,5)

        self.assertEqual(
            frac.sub(f1, f2).tostring(),
            'frac ( 1, 35 )'
        )

        self.assertEqual(
            frac.sub(f1, f1).tostring(),
            '0'
        )

        self.assertEqual(
            frac.sub(f2, f1).tostring(),
            '* ( -1, frac ( 1, 35 ) )'
        )


    def test_simplify(self):
        f = frac.fromints(24,60)
        self.assertEqual(
            frac._simplify(f).tostring(),
            'frac ( 2, 5 )'
        )


if __name__ == "__main__":
    unittest.main()
