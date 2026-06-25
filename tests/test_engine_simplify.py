import unittest
from cas import Expression
from cas import simplify

class TestSimplifyMethods(unittest.TestCase):

    @unittest.skip("To be implemented")
    def test_substitute(self):
        pass

    # @unittest.skip("To be implemented")
    def test_artitheticEval(self):
        a = Expression.fromstr('(7 - 2 * 3 + 3 ^ 2) / (5 * (2-1))')
        b = Expression.fromstr('4 ^ 3 + (3 ^ 2 - (10 / 2)) - 7 * 3')

        self.assertEqual(
            simplify.arithmeticEval(a).tostring(),
            '2'
        )

        self.assertCountEqual(
            simplify.arithmeticEval(b).tostring(),
            '47'
        )