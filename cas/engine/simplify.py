
from ..expression import Expression
from ..ast_node import ASTNode
from ..lexer import TokenType as TType
from ..lexer import Token, isnum, issym


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


def eval(expr: Expression) -> float | Exception:
    pass
