"""Functions involving Num Nodes"""

from ..ast_node import ASTNode


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


def sub(n1: ASTNode, n2: ASTNode):
    result = ASTNode.number(abs(int(n1) - int(n2)))

    return result if int(n1) >= int(n2) else neg(result)


def prod(n1: ASTNode, n2: ASTNode) -> ASTNode:
    """
    Find the product of two positive num nodes
    """

    return ASTNode.number(int(n1) * int(n2))


def iquot(n1: ASTNode, n2: ASTNode) -> ASTNode:
    """
    Find the integer quotient of positive integers n1 and n2 (n1 // n2)
    """

    return ASTNode.number(int(n1) // int(n2))


def fquot(n1: ASTNode, n2: ASTNode) -> ASTNode:
    """
    Find the fraction quotient of positive integers n1 and n2
    """

    return ASTNode.frac(n1, n2)


def rem(n1: ASTNode, n2: ASTNode) -> ASTNode:
    """
    Find the modulo of positive integers n1 and n2
    """

    return ASTNode.number(int(n1) % int(n2))


def ipow(n, p):
    """
    Find the power of two positive num nodes
    """

    return ASTNode.number(int(n) ** int(p))
