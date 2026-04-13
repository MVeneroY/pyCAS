'''
ast_nodes.py

'''

from typing_extensions import Self
from .lexer import TokenType
from .lexer import Token

class ASTNode:
    left: Self = None
    right: Self = None
    literal: str
    token_type: TokenType

    operator_map = {'+': 'Add',
                    '-': 'Sub',
                    '*': 'Mul',
                    '/': 'Div',
                    '^': 'Pow'}

    def __init__(self, literal: str, token_type: TokenType = None):
        self.literal = literal
        if token_type is not None: self.token_type = token_type
        else: self.token_type = Token.get_token_type(literal)

    @classmethod
    def fromtoken(cls, token: Token) -> Self:
        return cls(token.literal(), token.type())

    def __repr__(self):
        return f'Node({self.literal}, {self.token_type})'
    
    def ops_to_string(self) -> str:
        if self.token_type == TokenType.Operator and\
        self.left is not None and\
        self.right is not None:
            op_str = self.operator_map[self.literal]
            return f'{op_str}( {self.left.ops_to_string()}, {self.right.ops_to_string()} )'

        if self.token_type == TokenType.Number or\
        self.token_type == TokenType.Symbol:
            return f'{self.literal}'
        
    def print_op(self) -> None:
        print(self.ops_to_string())
    
    def _traverse(self, count: int) -> None:
        # if count > 10: return

        print('  ' * count, self)
        if self.left is not None: self.left._traverse(count + 1)
        if self.right is not None: self.right._traverse(count + 1)

    def traverse(self) -> None:
        self._traverse(0)