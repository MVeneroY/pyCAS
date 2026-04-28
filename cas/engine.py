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

'''
Currently only supports addition and subtraction between constants
'''
def arithmetic_engine(expr: Expression) -> Expression:
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
