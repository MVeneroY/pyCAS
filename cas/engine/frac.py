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

def fromnum(node: ASTNode) -> ASTNode:
    assert node.type() == TType.Num
    return ASTNode.frac(
        ASTNode.number(node.literal()),
        ASTNode.number(1)
    )


def fromints(n: int, d: int) -> ASTNode:
    return ASTNode.frac( ASTNode.number(n), ASTNode.number(d) )


def numerator(head: ASTNode) -> int:
    assert head.type() == TType.Frac
    return int(head.children()[0].literal())


def denominator(head: ASTNode) -> int:
    assert head.type() == TType.Frac
    return int(head.children()[1].literal())


def ratio(head: ASTNode) -> float:
    return numerator(head) / denominator(head)


def add(head1: ASTNode, head2: ASTNode) -> ASTNode:
    assert head1.type() == TType.Frac and head2.type() == TType.Frac

    _lcd = utils.lcd(
        denominator(head1),
        denominator(head2)
    )

    return fromints(round(_lcd * (ratio(head1) + ratio(head2))), _lcd)


def nadd(*addends: ASTNode) -> ASTNode:
    """
    n-ary fraction addition
    """

    _lcd = utils.nlcd(*[denominator(frac) for frac in addends])
    numerators = [numerator(frac) * int(_lcd / denominator(frac)) for frac in addends]

    res = fromints(
        reduce(operator.add, numerators), _lcd
    )

    return res


def sub(head1: ASTNode, head2: ASTNode) -> ASTNode:
    assert head1.type() == TType.Frac and head2.type() == TType.Frac

    _lcd = utils.lcd(
        denominator(head1),
        denominator(head2)
    )

    res = fromints(round(_lcd * (ratio(head1) - ratio(head2))), _lcd)

    if numerator(res) < 0 :
        _res = ASTNode.fromstr('*')
        _res.add_children([
            ASTNode.number(-1),
            fromints(
                abs(numerator(res)),
                denominator(res)
            )
        ])
        res = _res
    elif numerator(res) == 0:
        res = ASTNode.number(0)

    return res


def _simplify(head: ASTNode) -> ASTNode:
    num = numerator(head)
    den = denominator(head)
    if (_gcd := utils.gcd(num, den)) == 1:
        return head

    res = fromints(num // _gcd, den // _gcd)

    return res