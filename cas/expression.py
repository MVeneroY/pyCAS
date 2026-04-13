'''
expression.py
'''

from .ast_nodes import ASTNode
from .lexer import str_to_tokens
from .parser import _generate_expr
from typing_extensions import Self
import copy

class Expression():
    _expression: ASTNode = None
    
    def __init__(self, string: str):
        self._expression = _generate_expr((str_to_tokens(string)))

    def __repr__(self):
        return self._expression.ops_to_string()
    
    def copy(self) -> Self:
        return copy.deepcopy(self)