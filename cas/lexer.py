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

DEBUG = False

from enum import Enum
from cas.ast_nodes import ASTNode
from cas.parser import TokenType, get_token_type, next_token

def tokens_to_nodes(tokens: list[str]) -> list[ASTNode]:
    nodes = []

    for token in tokens:
        nodes.append(ASTNode(token))

    return nodes

def generate_expr(tokens: list[str]) -> ASTNode:
    '''
    Generates an expression from a list of tokens using the following grammar:

    expr    := term
            |  expr + term
            |  expr - term

    ex:
    3*x + 4 -> Add( Mul( 3, x ), 4 )
    1 + 2 + 3 -> Add( Add( 1, 2 ), 3 )
    x*-2 -2 -> Sub( Mul( x , Mul( -1, 2) ), 2 )
    '''
    def last_op(tokens: list[str]):
        curr = -1
        for index, token in enumerate(tokens):
            if token == '+':
                curr = index
            elif token == '-':
                if index > 0 and tokens[index-1] != '*' and tokens[index-1] != '/':
                    curr = index
        return curr
    
    if DEBUG: print('gen_expr', tokens)

    op_index = last_op(tokens)
    # print(tokens, op_index)
    if op_index == -1:
        return generate_term(tokens)
    
    head = ASTNode(tokens[op_index])
    head.right = generate_term(tokens[op_index+1:])
    head.left = generate_expr(tokens[0:op_index])
    return head


def generate_term(tokens: list[str]) -> ASTNode:
    '''
    (Currently) Generates a term from a list of tokens based on the following grammar:
    (Currently) factors only consist of monomials e.g. x, 4, -1, x^5 (no (x-1))

    term    := factor
            |  term * factor
            |  term / factor

    ex:
    2    -> 2
    2*3  -> Mul ( 2 , 3 )
    2 / 5 * x -> Mul ( Div ( 2, 5 ), x )
    2 * 5 * x -> Mul ( Mul ( 2, 5 ) , x )
    -2 * x -> Mul( Mul( -1, 2 ), x)
    '''
    def last_op(tokens: list[str]):
        curr = -1
        for index, token in enumerate(tokens):
            if token == '*' or token == '/':
                curr = index
        return curr

    if DEBUG: print('gen_term', tokens)

    '''
    base case: this is the last factor in the term
    '''
    op_index = last_op(tokens)
    if op_index == -1:
        return generate_factor(tokens)
    
    head = ASTNode(tokens[op_index])
    head.right = generate_factor(tokens[op_index+1:])
    head.left = generate_term(tokens[0:op_index])
    return head

def generate_factor(tokens: list[str], index: int = 0) -> ASTNode:
    '''
    returns: 
    ASTNode: head of the node tree
    int: index of the last used token

    (Currently) Generates a factor from a list of tokens based on the following grammar:

    factor  := -1 * factor
            |  symbol | number ^ symbol | number
            |  symbol | number

    ex:
    -2   -> Mul( -1, 2 )
    x**7 -> Pow( x, 7 )
    -x^3 -> Mul( -1, Pow( x, 3 ) )
    '''
    def last_op(tokens):
        curr = -1
        for index, token in enumerate(tokens):
            if token == '^':
                curr = index
        return curr

    if DEBUG: print('gen_fact', tokens)
    
    head = None
    i = index

    '''
    Negative numbers such as -2 are split into -1*2
    '''
    if tokens[0] == '-':
        head = ASTNode('*')
        head.left = ASTNode('-1', TokenType.Number)
        head.right = generate_factor(tokens[1:])
        return head
    
    # ''' Node: last working version
    # Powers (e.g. x^2) are represented as a single factor
    # '''
    # if len(tokens) > i + 2 and tokens[i+1] == '^':
    #     head = ASTNode('^')
    #     head.left = ASTNode(tokens[i])
    #     head.right = ASTNode(tokens[i+2])
    #     return head

    '''
    3x^2 -> Mul(3, Pow(x, 2))
    x^2 -> Pow(x,2)
    '''
    pow_index = last_op(tokens)
    if DEBUG: print(f'pow_index: {pow_index}')
    if pow_index != -1:
        head = ASTNode('^')
        head.right = ASTNode(tokens[pow_index+1]) # Note: only takes next token currently
        head.left = ASTNode(tokens[pow_index-1])

        if pow_index > 1:
            temp = head
            head = ASTNode('*')
            head.right = temp
            head.left = generate_factor(tokens[:pow_index-1])

        return head
    
    '''
    2x and xy are represented as 2*x and x*y
    '''
    if len(tokens) > 1:
        head = ASTNode('*')
        head.right = ASTNode(tokens[-1])
        head.left = generate_factor(tokens[:-1])
        return head

    return ASTNode(tokens[0])
