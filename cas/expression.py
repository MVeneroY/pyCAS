'''
expression.py
'''

from .ast_node import ASTNode
from .lexer import gettokens, Token
# from .parser import _generate_expr
from .parser import _parsetokens
from typing_extensions import Self
import copy

class Expression():
    _expression: ASTNode = None
    
    def __init__(self, tokens: list[Token]):
        self._expression = _parsetokens(tokens)

    @classmethod
    def fromstr(cls, string) -> Self:
        return cls(gettokens(string))

    def __repr__(self):
        return self._expression.tostring()
    
    def copy(self) -> Self:
        return copy.deepcopy(self)