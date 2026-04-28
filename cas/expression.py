"""
expression.py
"""

from .ast_node import ASTNode
from .lexer import gettokens, Token
from .lexer import TokenType as TType
from .parser import _parsetokens
from typing_extensions import Self
import copy


class Expression:
    _expression: ASTNode = None
    _kind: TType = None
    _tokenlist: list[Token] = None
    _syms: list[str] = None

    def __init__(self, node: ASTNode, tokenlist: list[Token] = None, symbols=None):
        self._expression = node
        self._kind = node.type()
        self._tokenlist = tokenlist
        if symbols:
            self._syms = symbols
        else:
            self._syms = node.getsymbols()

    @classmethod
    def fromtokens(cls, tokens: list[Token]) -> Self:
        node = _parsetokens(tokens)
        symbols = []
        for token in tokens:
            if token.type() == TType.Sym and token.literal() not in symbols:
                symbols.append(token.literal())
        return cls(node, tokens, symbols)

    @classmethod
    def fromstr(cls, string) -> Self:
        tokens = gettokens(string)
        node = _parsetokens(tokens)
        symbols = []
        for token in tokens:
            if token.type() == TType.Sym and token.literal() not in symbols:
                symbols.append(token.literal())
        return cls(node, tokens, symbols)

    def __repr__(self):
        return self._expression.tostring()
    
    def tostring(self):
        return self.__repr__()

    def kind(self) -> TType:
        return self._kind

    def copy(self) -> Self:
        return copy.deepcopy(self)
