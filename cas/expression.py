'''
expression.py
'''

from .ast_nodes import ASTNode
from .parser import str_to_tokens
from .lexer import generate_expr
from typing_extensions import Self
import copy

class Expression():
    _expression: ASTNode = None
    
    def __init__(self, head: ASTNode):
        self._expression = head

    def __init__(self, tokens: list[str]):
        self._expression = generate_expr(tokens)

    def __init__(self, string: str):
        self._expression = generate_expr((str_to_tokens(string)))

    def __repr__(self):
        return self._expression.ops_to_string()
    
    def copy(self) -> Self:
        return copy.deepcopy(self)