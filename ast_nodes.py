'''
ast_nodes.py

'''

from enum import Enum
from typing_extensions import Self
from parser import TokenType
from parser import get_token_type

# class NodeType(Enum):
#     Expression = 1
#     Factor = 2
#     Operator = 3
#     Number = 4
#     Symbol = 5

# class ASTNode():
#     literal: str
#     node_type: NodeType
#     children: list[Self] = None

#     def __init__(self, literal: str, node_type: NodeType):
#         self.literal = literal
#         self.node_type = node_type

'''
ASTNode:
    left: Self
    right: Self
    operation: str ('+', '-', etc)

'''

class ASTNode:
    left: Self = None
    right: Self = None
    token: str
    token_type: TokenType

    def __init__(self, token):
        self.token = token
        self.token_type = get_token_type(token)

    def __repr__(self):
        return f'Node({self.token}, {self.token_type})'
    
    def _traverse(self, count):
        if count > 10: return

        print('  ' * count, self)
        if self.left is not None: self.left._traverse(count + 1)
        if self.right is not None: self.right._traverse(count + 1)

    def traverse(self):
        self._traverse(0)