"""
ast_node.py
"""

from typing_extensions import Self
from cas.lexer import Token


class ASTNode:
    _token: Token
    _children: list[Self]

    def __init__(self, token: Token):
        self._token = token
        self._children = []

    def __str__(self):
        return f"{self._token.literal()}"
    
    def literal(self) -> str:
        return self._token.literal()
    
    def type(self) -> str:
        return self._token.type()

    def add_child(self, child: Self):
        self._children.append(child)

    def children(self):
        return self._children

    def tostring(self) -> str:
        if len(self._children) == 0:
            return f"{self._token._literal}"
        args = [child.tostring() for child in self._children]
        string = f"{self._token._literal} ( "
        for index, arg in enumerate(args):
            if index + 1 < len(args):
                string += f"{arg}, "
            else:
                string += f"{arg} )"
        return string

    def print(self):
        print(self.tostring())
