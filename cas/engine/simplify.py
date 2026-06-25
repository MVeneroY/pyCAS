"""
simplify.py
"""

from ..expression import Expression
from ..ast_node import ASTNode
from ..lexer import TokenType as TType
from ..lexer import Token, isnum, issym

from . import num
from . import frac


def substitute(expr: Expression, symbol: str, value: str) -> Expression | None:
    """
    Returns a new Expression object, where every instance of `symbol` is replaced with `value`
    """
    assert isnum(value) or issym(value)

    def _search(node: ASTNode, symbol: str, value: str) -> ASTNode:
        if node.has_children():
            for index, child in enumerate(node.children()):
                node.update_child(_search(child, symbol, value), index)
            return node

        elif node.type() == TType.Sym and node.literal() == symbol:
            return ASTNode(Token(value, TType.Sym if issym(value) else TType.Num))

        else:
            return node

    if symbol not in expr._syms:
        print(f"Symbol {symbol} not present in expression.")
        return None

    new_expr = _search(expr._expression, symbol, value)
    return Expression(new_expr, symbols=expr._syms[:].remove(symbol))


def arithmeticEval(expr: Expression) -> Expression:
    '''
    Evaluate an arithmetic expression and simplify
    '''
    _head = arithmeticParseNode(expr._expression)
    if _head.type() == TType.Frac:
        _head = frac.simplify(_head, keep_frac=False)

    return Expression.fromNode(_head)


def arithmeticParseNode(curr: ASTNode) -> ASTNode:
    '''
    Evaluate an arithmetic `ASTNode` tree
    '''
    if not all([is_leaf(child) for child in curr.children()]):
        _children = []
        for child in curr.children():
            if is_leaf(child):
                _children.append(child)
            else:
                _children.append(arithmeticParseNode(child))
        curr._children = _children

    return arithmeticEvalLeaves(curr)


def arithmeticEvalLeaves(parent: ASTNode) -> ASTNode:
    '''
    Evaluate the leaf nodes descending from the `parent` node arithmetically
    '''
    # Exponentiation identity
    if parent.type() == TType.Pow and parent.getChild(0).literal() == "1":
        return ASTNode.number(1)

    if parent.type() == TType.Pow and parent.getChild(1).literal() == "-1":
        if parent.getChild(0).type() == TType.Frac:
            node = frac.reciprocal(parent.getChild(0))
            return node

        node = frac.fromNodes(ASTNode.number(1), parent.getChild(0))
        return node

    if parent.type() == TType.Pow and parent.getChild(1).type() == TType.Num:
        node = num.ipow(parent.getChild(0), parent.getChild(1))
        return node

    # compute product
    if parent.type() == TType.Mul:
        if any([child.type() == TType.Frac for child in parent.children()]):
            # convert all numbers to fractions
            _children = []
            for child in parent.children():
                _child = child
                if _child.type() != TType.Frac:
                    _child = frac.fromNum(_child)
                _children.append(_child)

            return frac.nprod(_children)

        return num.nprod(parent.children())

    # compute addition
    if parent.type() == TType.Add:
        if any([child.type() == TType.Frac for child in parent.children()]):
            # convert all numbers to fractions
            _children = []
            for child in parent.children():
                _child = child
                if _child.type() != TType.Frac:
                    _child = frac.fromNum(_child)
                _children.append(_child)

            return frac.nadd(_children)

        return num.nadd(parent.children())

    print("returning None")
    return None


def is_leaf(node: ASTNode) -> bool:
    return not node.children()
