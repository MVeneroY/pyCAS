"""Functions involving Num Nodes"""

from ..ast_node import ASTNode
from . import frac
from functools import reduce


def neg(head: ASTNode) -> ASTNode:
    """
    Returns the negative of a tree
    """

    _head = ASTNode.fromstr("*")
    _head.add_child(ASTNode.number(-1))
    _head.add_child(head)

    return _head


def add(n1: ASTNode, n2: ASTNode) -> ASTNode:
    return ASTNode.number(int(n1) + int(n2))


def nadd(operands: list[ASTNode]) -> ASTNode:
    return ASTNode.number(reduce(add, operands))


def sub(n1: ASTNode, n2: ASTNode):
    result = ASTNode.number(abs(int(n1) - int(n2)))

    return result if int(n1) >= int(n2) else neg(result)


def prod(n1: ASTNode, n2: ASTNode) -> ASTNode:
    """
    Find the product of two positive num nodes
    """

    return ASTNode.number(int(n1) * int(n2))


def nprod(operands: list[ASTNode]) -> ASTNode:
    return reduce(prod, operands)


def iquot(n1: ASTNode, n2: ASTNode) -> ASTNode:
    """
    Find the integer quotient of positive integers n1 and n2 (n1 // n2)
    """

    return ASTNode.number(int(n1) // int(n2))


def div(n1: ASTNode, n2:ASTNode) -> ASTNode:
    '''
    Return an integer or frac node equivalent to n1 / n2
    '''

    return frac.simplify(frac.fromInts(n1, n2), keep_frac=False)


def rem(n1: ASTNode, n2: ASTNode) -> ASTNode:
    """
    Find the modulo of positive integers n1 and n2
    """

    return ASTNode.number(int(n1) % int(n2))


def ipow(n: ASTNode, p: ASTNode):
    """
    Find the power of two positive num nodes
    """

    return ASTNode.number(int(n) ** int(p))
