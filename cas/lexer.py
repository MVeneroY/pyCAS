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

from cas.ast_nodes import ASTNode
from cas.parser import TokenType

def tokens_to_nodes(tokens: list[str]) -> list[ASTNode]:
    nodes = []

    for token in tokens:
        nodes.append(ASTNode(token))

    return nodes

def generate_factor(tokens: list[str], index: int = 0) -> ASTNode:
    '''
    (Currently) Generates a factor from a list of tokens based on the following grammar:

    factor  := -1 * factor
            |  symbol | number ^ symbol | number
            |  symbol | number

    ex:
    -2 -> Mul( -1, 2 )

    x**7 -> Pow( x, 7 )

    -x^3 -> Mul( -1, Pow( x, 3 ) )
    '''
    
    head = None
    i = index

    '''
    Negative numbers such as -2 are split into -1*2
    '''
    if tokens[i] == '-':
        head = ASTNode('*')
        head.left = ASTNode('-1', TokenType.Number)
        head.right = generate_factor(tokens, index + 1)
        return head
    
    '''
    Powers (e.g. x^2) are represented as a single factor
    '''
    if len(tokens) > i + 2 and tokens[i+1] == '^':
        head = ASTNode('^')
        head.left = ASTNode(tokens[i])
        head.right = ASTNode(tokens[i+2])
        return head
    
    return ASTNode(tokens[i])
