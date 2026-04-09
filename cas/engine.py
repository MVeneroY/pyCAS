'''
engine.py
'''

from .expression import Expression
from .ast_nodes import ASTNode

def substitute(expr: Expression, symbol: str, value: str) -> Expression:
    '''
    Returns a new Expression object, where every instance of `symbol` is replaced with `value`
    
    Currently doesn't support:
    negative values e.g. replace x with -2
    expressions e.g. replace x with 2y+10
    '''

    def _search(_node: ASTNode, symbol: str, value: str) -> ASTNode:
        if _node.left is not None: _node.left = _search(_node.left, symbol, value)
        if _node.right is not None: _node.right = _search(_node.right, symbol, value)

        if _node.literal == symbol:
            new_node = ASTNode(value)
            new_node.left = _node.left
            new_node.right = _node.right
            return new_node
        
        return _node

    if float(value) < 0:
        raise NotImplementedError()
    expr_copy = expr.copy()
    _search(expr_copy._expression, symbol, str(value))
    return expr_copy

def evaluate(expr: Expression) -> float | Exception:
    '''
    Evaluate a numerical expression
    TODO: evaluate decimal values as fractions to maintain precision
    '''

    def _evaluate(node: ASTNode) -> float | Exception:
        if node.left.left is not None and node.left.right is not None:
            node.left = ASTNode(str(_evaluate(node.left)))
        if node.right.left is not None and node.right.right is not None:
            node.right = ASTNode(str(_evaluate(node.right)))

        match node.literal:
            case '+': return float(node.left.literal) + float(node.right.literal)
            case '-': return float(node.left.literal) - float(node.right.literal)
            case '*': return float(node.left.literal) * float(node.right.literal)
            case '/': return float(node.left.literal) / float(node.right.literal)
            case '^': return float(node.left.literal) ** float(node.right.literal)
            case _: raise Exception()

    return _evaluate(expr._expression)