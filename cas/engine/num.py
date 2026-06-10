'''Functions involving Num Nodes'''

from ..ast_node import ASTNode

def add(n1: ASTNode, n2: ASTNode) -> ASTNode:
    return ASTNode.number(int(n1) + int(n2))

def sub(n1, n2):
    pass

def prod(n1, n2):
    pass

def quot(n1, n2):
    pass

def ipow(n, p):
    pass