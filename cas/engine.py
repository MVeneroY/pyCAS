'''
engine.py
'''

from .expression import Expression
from .ast_node import ASTNode

def substitute(expr: Expression, symbol: str, value: str) -> Expression:
    '''
    Returns a new Expression object, where every instance of `symbol` is replaced with `value`
    '''
    pass

def evaluate(expr: Expression) -> float | Exception:
    '''
    Evaluate a numerical expression
    '''

    pass