import unittest
from cas.ast_node import ASTNode
from cas.engine import frac
from cas.engine import num
from cas.expression import Expression

class TestNumMethods(unittest.TestCase):
   
    def test_add(self):
        n1 = ASTNode.number(3)
        n2 = ASTNode.number(5)

        self.assertEqual(
            num.add(n1, n2).tostring(),
            '8'
        )

    def test_nadd(self):
        nums = [ASTNode.number(n) for n in range(1,10)]

        self.assertEqual(
            num.nadd(nums).tostring(),
            '45'
        )
    
    def test_sub(self):
        n1 = ASTNode.number(3)
        n2 = ASTNode.number(1)

        self.assertEqual(
            num.sub(n1, n2).tostring(),
            '2'
        )

        self.assertEqual(
            num.sub(n1, n1).tostring(),
            '0'
        )

        self.assertEqual(
            num.sub(n2, n1).tostring(),
            '* ( -1, 2 )'
        )

    def test_prod(self):
        n1 = ASTNode.number(4)
        n2 = ASTNode.number(6)

        self.assertEqual(
            num.prod(n1, n2).tostring(),
            '24'
        )

    def test_iquot(self):
        n1 = ASTNode.number(4)
        n2 = ASTNode.number(3)

        self.assertEqual(
            num.iquot(n1, n2).tostring(),
            '1'
        )

    def test_div(self):
        n1 =  ASTNode.number(3)
        n2 = ASTNode.number(6)

        self.assertEqual(
            num.div(n1, n2).tostring(),
            'frac ( 1, 2 )'
        )

        self.assertEqual(
            num.div(n2, n1).tostring(),
            '2'
        )

    def test_ipow(self):
        n = ASTNode.number(3)
        p = ASTNode.number(4)

        self.assertEqual(
            num.ipow(n, p).tostring(),
            '81'
        )


if __name__ == "__main__":
    unittest.main()
