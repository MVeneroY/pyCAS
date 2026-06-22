'''
frac.py

Frac nodes consist of numbers only. Ratios between other node types are represented as divisions
'''

from .. import ast_node
from .. import lexer
from . import utils

from ..ast_node import ASTNode
from ..lexer import TokenType as TType

from functools import reduce
import operator

def fromNum(node: ASTNode) -> ASTNode:
    assert node.type() == TType.Num
    return ASTNode.frac(
        ASTNode.number(node.literal()),
        ASTNode.number(1)
    )


def fromNodes(n: ASTNode, d: ASTNode) -> ASTNode:
    return ASTNode.frac(n, d)


def fromInts(n: int, d: int) -> ASTNode:
    return ASTNode.frac( ASTNode.number(n), ASTNode.number(d) )


def numerator(head: ASTNode) -> int:
    assert head.type() == TType.Frac
    return int(head.children()[0].literal())


def denominator(head: ASTNode) -> int:
    assert head.type() == TType.Frac
    return int(head.children()[1].literal())


def fratio(head: ASTNode) -> float:
    return numerator(head) / denominator(head)


def add(head1: ASTNode, head2: ASTNode) -> ASTNode:
    assert head1.type() == TType.Frac and head2.type() == TType.Frac

    _lcd = utils.lcd(
        denominator(head1),
        denominator(head2)
    )

    return fromInts(round(_lcd * (fratio(head1) + fratio(head2))), _lcd)


def nadd(addends: ASTNode) -> ASTNode:
    """
    n-ary fraction addition
    """

    _lcd = utils.nlcd([denominator(frac) for frac in addends])
    numerators = [numerator(frac) * int(_lcd / denominator(frac)) for frac in addends]

    res = fromInts(
        reduce(operator.add, numerators), _lcd
    )

    return res


def sub(head1: ASTNode, head2: ASTNode) -> ASTNode:
    assert head1.type() == TType.Frac and head2.type() == TType.Frac

    _lcd = utils.lcd(
        denominator(head1),
        denominator(head2)
    )

    res = fromInts(round(_lcd * (fratio(head1) - fratio(head2))), _lcd)

    if numerator(res) < 0 :
        _res = ASTNode.fromstr('*')
        _res.add_children([
            ASTNode.number(-1),
            fromInts(
                abs(numerator(res)),
                denominator(res)
            )
        ])
        res = _res
    elif numerator(res) == 0:
        res = ASTNode.number(0)

    return res


def prod(f1: ASTNode, f2: ASTNode) -> ASTNode:
    '''
    Find the product between two positive Fraction trees
    '''

    return fromInts(
        numerator(f1) * numerator(f2),
        denominator(f1) * denominator(f2)
    )


def nprod(operands: list[ASTNode]) -> ASTNode:
    return reduce(prod, operands)


def quot(f1: ASTNode, f2: ASTNode) -> ASTNode:

    return fromInts(
        numerator(f1) * denominator(f2),
        denominator(f1) * numerator(f2)
    )


def ipow(f: ASTNode, p: ASTNode) -> ASTNode:
    '''
    Find the power of a positive fraction tree. To be a private function
    '''
    assert p.type() == TType.Num

    return fromInts(
        numerator(f) ** int(p),
        denominator(f) ** int(p)
    )


def simplify(head: ASTNode, keep_frac: bool = True) -> ASTNode:
    num = numerator(head)
    den = denominator(head)
    if (_gcd := utils.gcd(num, den)) == 1:
        return head

    res = fromInts(num // _gcd, den // _gcd)

    if not keep_frac and denominator(res) == 1:
        return res.children()[0]
    return res