"""
lexer.py
"""

from enum import Enum
import regex as re


class TokenType(Enum):
    Sym = 1  # x, y
    Num = 2
    Frac = 3
    Add = 4
    Sub = 5
    Mul = 6
    Div = 7
    Pow = 8
    Rem = 9
    Fac = 10
    Eq = 11
    GT = 12
    GEQ = 13
    LT = 14
    LEQ = 15
    NEQ = 16
    AND = 17
    OR = 18
    NOT = 19
    SIN = 20
    COS = 21
    TAN = 22
    LPAR = 23
    RPAR = 24
    SQRT = 25


tokentype_map = {
    "+": TokenType.Add,
    "-": TokenType.Sub,
    "*": TokenType.Mul,
    "/": TokenType.Div,
    "^": TokenType.Pow,
    "%": TokenType.Rem,
    "!": TokenType.Fac,
    "(": TokenType.LPAR,
    ")": TokenType.RPAR,
    "sin": TokenType.SIN,
    "cos": TokenType.COS,
    "tan": TokenType.TAN,
    "sqrt": TokenType.SQRT,
    "frac": TokenType.Frac
}


class Symbol:
    namespace = None

    def __init__(self):
        self.namespace = []

    def symbols(string: str) -> None:
        for symbol in string.split():
            if symbol not in Symbol.namespace:
                Symbol.namespace.append(symbol)


class Token:
    _literal: str
    _type: TokenType

    def __init__(self, literal: str, type: TokenType):
        self._literal = literal
        self._type = type

    def __int__(self) -> int:
        assert self._type == TokenType.Num
        return int(self._literal)

    def literal(self) -> str:
        return self._literal

    def type(self) -> TokenType:
        return self._type


def gettokens(string: str) -> list[Token]:
    """Tokenize an expression and return a list of Token objects

    Args:
        string (str): expression string

    Returns:
        list[Token]: tokenized expression
    """

    """
    Raw string modifications:
    blank spaces are removed
    ** -> ^
    """
    string = string.replace(" ", "").replace("**", "^")
    string = re.sub(r"\+{2,}", r"\+", string)

    matches = [
        match
        for match in re.findall(
            r"[\+\-\*\/\^\(\)]|sqrt|sin|cos|tan|\d*\.?\d*|[a-zA-Z]{1}", string
        )
        if match != ""
    ]

    tokens = []
    for match in matches:
        if match in tokentype_map:
            tokens.append(Token(match, tokentype_map[match]))
        elif isnum(match):
            tokens.append(Token(match, TokenType.Num))
        elif issym(match):
            tokens.append(Token(match, TokenType.Sym))

    return tokens


def isnum(string: str) -> bool:
    match = re.match(r"\d*\.?\d*", string)
    return match and match[0] == string


def issym(string: str) -> bool:
    match = re.match(r"[a-zA-z]{1}", string)
    return match and match[0] == string
