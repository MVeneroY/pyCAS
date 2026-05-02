"""
engine.py
"""

from .expression import Expression
from .ast_node import ASTNode
from .lexer import TokenType as TType
from .lexer import Token, isnum, issym


def subs(expr: Expression, symbol: str, value: str) -> Expression | None:
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


def eval(expr: Expression) -> float | Exception:
    """
    Evaluate a numerical expression
    """

    pass


def arithmetic_engine(expr: Expression) -> Expression:
    """
    Currently only supports addition and subtraction between constants
    """
    expr2 = expr.copy()

    kind = expr2.kind()
    match kind:
        case TType.Add:
            resultant = 0
            i_buffer = []

            for index, child in enumerate(expr2._expression.children()):
                if child.type() == TType.Num:
                    resultant += float(child.literal())
                    i_buffer.append(index)

                # negative terms
                elif (
                    child.type() == TType.Mul
                    and len(child.children()) == 2
                    and child.children()[0].literal() == "-1"
                ):
                    resultant -= float(child.children()[1].literal())
                    i_buffer.append(index)

            if len(i_buffer) == len(expr2._expression.children()):
                return ASTNode(Token(str(resultant), TType.Num))

            for index in i_buffer[::-1]:
                expr2._expression.remove_child(index)
            expr2._expression.add_child(ASTNode(Token(str(resultant), TType.Num)))
            return expr2
        case _:
            pass


def numerator(head: ASTNode) -> int:
    assert head.type() == TType.Frac
    return int(head.children()[0].literal())


def denominator(head: ASTNode) -> int:
    assert head.type() == TType.Frac
    return int(head.children()[1].literal())


def gcd(n1: int, n2: int) -> int:
    if n1 == 0 or n2 == 0:
        return n1 + n2
    return gcd(n2, n1 % n2)


def lcd(n1: int, n2: int) -> int:
    return int(n1 * n2 / gcd(n1, n2))


def _frac_add(head1: ASTNode, head2: ASTNode) -> ASTNode:
    assert head1.type() == TType.Frac and head2.type() == TType.Frac

    num1 = numerator(head1)
    den1 = denominator(head1)
    num2 = numerator(head2)
    den2 = denominator(head2)

    if den1 != den2:
        _lcd = lcd(den1, den2)
        num1 *= int(_lcd / den1)
        num2 *= int(_lcd / den2)
        den1 = den2 = _lcd

    res = ASTNode(Token("frac", TType.Frac))
    res.add_child(ASTNode(Token(str(num1 + num2), TType.Num)))
    res.add_child(ASTNode(Token(str(den1), TType.Num)))
    return res


def _simplify_frac(head: ASTNode) -> ASTNode:
    # TODO: implement node object creation methods
    res = ASTNode(Token("frac", TType.Frac))
    n = numerator(head)
    d = denominator(head)
    _gcd = gcd(n, d)
    if _gcd == 1:
        return head

    res.add_child(ASTNode(Token(str(int(n / _gcd)), TType.Num)))
    res.add_child(ASTNode(Token(str(int(d / _gcd)), TType.Num)))
    return res

def _simplifymul(head: ASTNode) -> ASTNode:
    """Transforms a multiplication node to contain only 1 coefficient or fraction
    TODO: simplify nested multiplications e.g. * ( * (2, 3), 4, x ) -> * ( 24, x )
    
    Args:
        head (ASTNode): head of multiplication node

    Returns:
        ASTNode: new multiplication node
    """    
    res = ASTNode.fromstr('*')

    assert head.type() == TType.Mul
    coefficient_num = 1
    coefficient_den = 1

    for child in head.children()[::-1]:
        if child.type() == TType.Num:
            coefficient_num *= int( child.literal() )
        elif child.type() == TType.Pow and (gc:=child.children())[0].type() == TType.Num and gc[1].literal() == '-1':
            coefficient_den *= int ( gc[0].literal() )
        else:
            print(child.literal())
            res.add_child(child)

    if coefficient_den == 1:
        res.insert_child(0, ASTNode(Token(coefficient_num, TType.Num)))
    else:
        fnode = ASTNode.fromstr('frac')
        fnode.add_child(ASTNode(Token(str(coefficient_num), TType.Num)))
        fnode.add_child(ASTNode(Token(str(coefficient_den), TType.Num)))

        if len(res.children()) == 0: return fnode
        res.insert_child(0, _simplify_frac(fnode))

    return res
