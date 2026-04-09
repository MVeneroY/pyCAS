'''
parser.py

'''

from enum import Enum
import regex as re

class TokenType(Enum):
    Number = 1
    Symbol = 2
    Operator = 3

class Token():
    _literal: str
    _token_type: TokenType

    def __init__(self, literal: str):
        self._literal = literal
        self._token_type = Token.get_token_type(literal)

    def __repr__(self) -> str:
        return self._literal
    
    def __str__(self) -> str:
        return self._literal
    
    def literal(self) -> str:
        return self._literal

    def type(self) -> TokenType:
        return self._token_type

    def get_token_type(string: str) -> TokenType:
        '''
        Note: Only supports 1-letter alphabetic strings
        '''
        if isoperator(string): return TokenType.Operator
        if is_numeric(string): return TokenType.Number
        if string.isalpha() and len(string) == 1: return TokenType.Symbol
        return None


def isoperator(string: str) -> bool:
    return string == "+" or\
    string == "-" or\
    string == "*" or\
    string == "/" or\
    string == "^" or\
    string == "(" or\
    string == ")"
    
def is_symbol(string: str) -> bool:
    return len(string) == 1 and string.isalpha()

def is_numeric(string: str) -> bool:
    match = re.match(pattern=r'\d*\.?\d+', string=string) 
    return match is not None and match.captures()[0] == string

# def next_char(string: str, i: int) -> str:
#     if len(string) - 1 == i: return ""
#     return string[i+1]

def str_to_tokens(string: str) -> list[Token]:
    '''
    Returns a list of Token objects from a string
    '''
    
    tokens: list[Token] = []
    string = string.replace('**', '^').replace(' ', '')

    '''
    Non numerical indices. Currently relies on the restriction that all symbols
    be of length 1.
    '''
    non_num_indices: list[tuple[int, TokenType]] = [
        (index, token_type) for \
        (index, item) in enumerate(string) if\
        (token_type := Token.get_token_type(item)) == TokenType.Symbol or\
        token_type == TokenType.Operator
        ]
    
    '''
    If there are non numerical tokens in the string, the string consists of a single number
    '''
    if len(non_num_indices) == 0: 
        return [Token(string)]

    '''
    numerical index slices. Includes all whole number and decimal values
    '''
    num_index_slices: list[tuple[int, int]] = []
    if non_num_indices[0][0] > 0:
        num_index_slices.append((0,non_num_indices[0][0]))
    num_index_slices.extend([(start+1, end) for ((start, _), (end, _)) in\
                              zip(non_num_indices[0:-1], non_num_indices[1:]) if\
                                end > start+1])
    if non_num_indices[-1][0] < len(string):
        num_index_slices.append((non_num_indices[-1][0] + 1, len(string)))

    index = 0
    while index < len(string) and (len(non_num_indices) > 0 or len(num_index_slices) > 0):
        if len(non_num_indices) > 0 and index == non_num_indices[0][0]:
            tokens.append(Token(string[non_num_indices.pop(0)[0]]))
            index += 1
        elif len(num_index_slices) > 0 and index == num_index_slices[0][0]:
            start, end = num_index_slices.pop(0)
            tokens.append(Token(string[start:end]))
            index = end

    return tokens

def next_token(tokens: list[str], i: int) -> str:
    '''
    Returns tokens[i+1]
    If tokens[i] is the last item in the array, returns None
    '''

    if len(tokens) > i + 1: return tokens[i+1]
    return None