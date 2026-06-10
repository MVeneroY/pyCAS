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

    @unittest.skip("Might not be implemented")
    def test_nadd(self):
        pass
    
    @unittest.skip("Not implemented yet")
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
            frac.sub(n2, n1).tostring(),
            '* ( -1, 2 )'
        )

    @unittest.skip("Not implemented yet")
    def test_prod(self):
        n1 = ASTNode.number(4)
        n2 = ASTNode.number(6)

        self.assertEqual(
            num.prod(n1, n2).tostring(),
            '24'
        )

    @unittest.skip("Not implemented yet")
    def test_quot(self):
        '''
        TODO: consider different scenarios e.g. division by 0, modulo, remainder, etc
        '''
        f1 =  frac.fromInts(3,4)
        f2 = frac.fromInts(5,3)

        self.assertEqual(
            frac.quot(f1, f2).tostring(),
            'frac ( 9, 20 )'
        )

    @unittest.skip("Not implemented yet")
    def test_ipow(self):
        n = ASTNode.number(3)
        p = ASTNode.number(4)

        self.assertEqual(
            frac.ipow(n, p).tostring(),
            '81'
        )


if __name__ == "__main__":
    unittest.main()
