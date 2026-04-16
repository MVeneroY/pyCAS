'''
expression.py
'''

from ._ast_node import _ASTNode
from .lexer import gettokens
from .parser import _generate_expr
from typing_extensions import Self
import copy

class Expression():
    _head: _ASTNode = None
    
    def __init__(self, string: str):
        self._expression = _generate_expr((gettokens(string)))

    # def __repr__(self):
    #     return self._expression.ops_to_string()
    
    def copy(self) -> Self:
        return copy.deepcopy(self)