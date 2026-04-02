'''
Grammar:

expr    := term
        |  expr + term
        |  expr - term

term    := factor
        |  term * factor
        |  term / factor

factor  := number
        |  variable
        |  factor ^ number
        |  - factor

number  := (0-9)+

symbol  := (a-z)
'''

from ast_nodes import ASTNode

def tokens_to_nodes(tokens: list[str]) -> list[ASTNode]:
    nodes = []

    for token in tokens:
        nodes.append(ASTNode(token))

    return nodes

def generate_factor(tokens: list[str], index: int) -> ASTNode:
    
    head = None
    i = index
    if tokens[i] == '-':
        head = ASTNode('*')
        head.left = ASTNode('-1')
        head.right = generate_factor(tokens, index + 1)
        return head
    
    if len(tokens) > i + 2 and tokens[i+1] == '^':
        head = ASTNode('^')
        head.left = ASTNode(tokens[i])
        head.right = ASTNode(tokens[i+2])
        return head
    
    return ASTNode(tokens[i])

generate_factor(['-', 'x', '^', '3'], 0).traverse()
