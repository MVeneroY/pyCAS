"""
ast_node.py
"""

from typing_extensions import Self
from cas.lexer import Token
from cas.lexer import TokenType as TType
from cas.lexer import tokentype_map

class ASTNode:
    _token: Token
    _children: list[Self]

    def __init__(self, token: Token):
        self._token = token
        self._children = []

    @classmethod
    def fromstr(cls, string: str) -> Self:
        return cls(Token(string, tokentype_map[string]))
    
    @classmethod
    def frac(cls, num: Self, den: Self) -> Self:
        obj = cls.fromstr("frac")
        obj.add_children([num, den])
        return obj
    
    @classmethod
    def number(cls, n: int) -> Self:
        return cls(Token(str(n), TType.Num))

    def __str__(self):
        return f"{self._token.literal()}"
    
    def __int__(self):
        return int(self._token)

    def literal(self) -> str:
        return self._token.literal()

    def type(self) -> str:
        return self._token.type()

    def add_child(self, child: Self):
        self._children.append(child)

    def insert_child(self, index: int, child: Self):
        self._children.insert(index, child)

    def remove_child(self, index: int):
        self._children.pop(index)

    def update_child(self, new_child: Self, index: int):
        self._children[index] = new_child

    def has_children(self) -> bool:
        return self._children is not None and len(self._children) > 0

    def add_children(self, children: list[Self]):
        self._children = children

    def children(self):
        return self._children

    def getsymbols(self):
        if not self.has_children():
            if self.type() == TType.Sym:
                return [self.literal()]
            else:
                return []

        symbols = []
        for child in self.children():
            if child is None:
                continue
            child_sym = child.getsymbols()
            for sym in child_sym:
                if sym not in symbols:
                    symbols.append(sym)

        return symbols

    def tostring(self) -> str:
        if len(self._children) == 0:
            return f"{self._token._literal}"
        args = [child.tostring() for child in self._children if child is not None]
        string = f"{self._token._literal} ( "
        for index, arg in enumerate(args):
            if index + 1 < len(args):
                string += f"{arg}, "
            else:
                string += f"{arg} )"
        return string

    def print(self):
        print(self.tostring())
