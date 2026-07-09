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


def is_leaf(node: ASTNode) -> bool:
    return not node.children()


###############################################################################
#                      Arithmetic Simplification Methods                      #
###############################################################################


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
    op = parent.type()
    nodes = parent.children()

    return arithmeticEvalNodes(op, nodes)


def arithmeticEvalNodes(op: TType, nodes: list[ASTNode]) -> ASTNode:
    # Exponentiation identity
    if op == TType.Pow and nodes[0].literal() == "1":
        return ASTNode.number(1)

    if op == TType.Pow and nodes[1].literal() == "-1":
        if nodes[0].type() == TType.Frac:
            node = frac.reciprocal(nodes[0])
            return node

        node = frac.fromNodes(ASTNode.number(1), nodes[0])
        return node

    if op == TType.Pow and nodes[1].type() == TType.Num:
        node = num.ipow(nodes[0], nodes[1])
        return node

    # compute product
    if op == TType.Mul:
        if any([node.type() == TType.Frac for node in nodes]):
            # convert all numbers to fractions
            _nodes = []
            for node in nodes:
                _node = node
                if _node.type() != TType.Frac:
                    _node = frac.fromNum(node)
                _nodes.append(_node)

            return frac.nprod(_nodes)

        return num.nprod(nodes)

    # compute addition
    if op == TType.Add:
        if any([node.type() == TType.Frac for node in nodes]):
            # convert all numbers to fractions
            _nodes = []
            for node in nodes:
                _node = node
                if _node.type() != TType.Frac:
                    _node = frac.fromNum(_node)
                _nodes.append(_node)

            return frac.nadd(_nodes)

        return num.nadd(nodes)

    print("returning None")
    return None


###############################################################################
#                       Symbolic Simplification Methods                       #
###############################################################################


def termToDict(term: ASTNode) -> dict:
    '''
    Returns a dictionary containing the `coefficient` and `term` (variable factors) from a Node
    '''

    if term.type() == TType.Num:
        data = {
            "term": "num",
            "coefficient": int(term)
        }
    
    symbols = []
    data = {}
    if term.type() == TType.Mul:
        for child in term.children():
            if child.type() == TType.Num:
                if "coefficient" not in data:
                    data["coefficient"] = int(child)
                else:
                    data["coefficient"] *= int(child)
            else:
                symbols.append(child)

    term = ""
    term_data = factorsToDict(symbols)
    for base, power in term_data.items():
        term += f"{base}^{power}"
    data["term"] = term

    return data

def factorsToDict(terms: list[ASTNode]) -> dict:
    '''
    Returns a dictionary containing the simplified variable factors from a list of Nodes
    '''

    assert not any([term.type() == TType.Num for term in terms])
    factors = {}
    for term in terms:
        if term.type() == TType.Sym:
            if term.literal() not in factors:
                factors[term.literal()] = 1
            else:
                factors[term.literal()] += 1

        if term.type() == TType.Pow:
            base = term.getChild(0)
            power = term.getChild(1)
            if base.literal() not in factors:
                factors[base.literal()] = int(power)
            else:
                factors[base.literal()] += int(power)

    return dict(sorted(factors.items()))

# TODO: Implement support for subtraction, division
def addLikeTerms(terms: list[ASTNode]) -> ASTNode:
    '''
    Add terms based on their variables and powers
    '''

    result = {}

    for term in terms:
        data = termToDict(term)
        if data["term"] in result:
            result[data["term"]] += data["coefficient"]
        else:
            result[data["term"]] = data["coefficient"]

    head = None

    if len(result) > 1:
        head = ASTNode.fromstr('+')
        for _term, _coefficient in result.items():
            if int(_coefficient) == 1:
                head.add_child(Expression.fromstr(_term)._expression)
            else:
                temp = ASTNode.fromstr('*')
                temp.add_child(ASTNode.number(_coefficient))
                temp.add_child(Expression.fromstr(_term)._expression)
                head.add_child(temp)
    
    else:
        _term, _coefficient = list(result.items())[0]
        if int(_coefficient) == 1:
                head = Expression.fromstr(_term)._expression
        else:
            head = ASTNode.fromstr('*')
            head.add_child(ASTNode.number(_coefficient))
            head.add_child(Expression.fromstr(_term)._expression)

    return head

