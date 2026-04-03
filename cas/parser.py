'''
parser.py

TODO: implement support for decimal value numbers e.g. '3.2'
'''

from enum import Enum

class TokenType(Enum):
    Number = 1
    Symbol = 2
    Operator = 3

def isoperator(string: str) -> bool:
    return string == "+" or\
    string == "-" or\
    string == "*" or\
    string == "/" or\
    string == "^" or\
    string == "(" or\
    string == ")"
    

def get_token_type(string: str) -> TokenType:
    if isoperator(string): return TokenType.Operator
    if string.isnumeric(): return TokenType.Number
    if string.isalpha(): return TokenType.Symbol
    return None

def next_char(string: str, i: int) -> str:
    if len(string) - 1 == i: return ""
    return string[i+1]

def str_to_tokens(string: str) -> list[str]:

    tokens = []
    buffer = ""
    
    index = 0
    while index < len(string):

        if buffer == "":
            buffer += string[index]

        match get_token_type(buffer):
            case TokenType.Number:
                while get_token_type(next_char(string, index)) == TokenType.Number:
                    buffer += next_char(string, index)
                    index += 1
                tokens.append(buffer)
                index += 1
                buffer = ""

            case TokenType.Operator:
                if buffer == "*" and next_char(string, index) == '*':
                    buffer = "^"
                    index += 1
                tokens.append(buffer)
                index += 1
                buffer = ""

            case TokenType.Symbol:
                tokens.append(buffer)
                index += 1
                buffer =""

            case _:
                buffer = ""
                index+= 1

    return tokens
