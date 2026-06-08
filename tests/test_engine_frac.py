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


if __name__ == "__main__":
    unittest.main()
