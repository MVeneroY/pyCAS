"""
_parser_balance.py
"""

from cas.ast_node import ASTNode
from cas.lexer import gettokens, Token
from cas.lexer import TokenType as TType

DEBUG = 0


def _parsetokens(tokens: list[Token]) -> ASTNode:
    """Parse tokens from an expression and return an AST tree

    Args:
        tokens (list[Token]): Tokenized expression

    Returns:
        ASTNode: Head of the AST tree
    """
    if DEBUG:
        print("parse tokens:", [token.literal() for token in tokens])

    head: ASTNode = None
    pm_indices = [
        index
        for (index, token) in enumerate(tokens)
        if index > 0
        and is_pm(token)
        and not is_op(tokens[index - 1])
        and not token_inside_par(tokens, index)
    ]

    """
    Case: only 1 term in expression
    """
    if not pm_indices:
        # if expression := (expression), remove parenthesis
        if (
            len(tokens) > 1
            and tokens[0].type() == TType.LPAR
            and find_closing_par(tokens) == len(tokens) - 1
        ):
            return _parsetokens(tokens[1:-1])

        # leading negative
        if tokens[0].type() == TType.Sub:
            return neg_term(tokens[1:])

        # leading plus symbol
        if tokens[0].type() == TType.Add:
            return _parsetokens(tokens[1:])

        return _parse_term(tokens)

    """
    Case: multiple terms in expression
    """
    head = ASTNode(Token("+", TType.Add))
    i = 0
    pm_index = -1
    while i < len(tokens):
        if pm_indices:
            # ignore leading +
            if pm_index == -1 and tokens[0].type() == TType.Add:
                i += 1
            # account for leading -
            elif pm_index == -1 and tokens[0].type() == TType.Sub:
                pm_index = pm_indices.pop(0)
                head.add_child(neg_term(tokens[i + 1 : pm_index]))
                i = pm_index + 1
            else:
                if tokens[pm_index].type() == TType.Sub:
                    pm_index = pm_indices.pop(0)
                    head.add_child(neg_term(tokens[i:pm_index]))
                else:
                    pm_index = pm_indices.pop(0)
                    head.add_child(_parsetokens(tokens[i:pm_index]))
                i = pm_index + 1

        elif pm_index != -1:
            if tokens[pm_index].type() == TType.Sub:
                head.add_child(neg_term(tokens[i:]))
            else:
                head.add_child(_parsetokens(tokens[i:]))
            break
    return head


def _parse_term(term: list[Token]) -> ASTNode:
    """Parse tokens from a term and return an AST tree

    Args:
        term (list[Token]): tokenized term

    Returns:
        ASTNode: head of an AST tree
    """
    if DEBUG:
        print("parse term:", [token.literal() for token in term])

    md_indices = [
        index
        for (index, token) in enumerate(term)
        if (token.type() == TType.Mul or token.type() == TType.Div)
        and not token_inside_par(term, index)
    ]

    """
    base case: no * or / signs
    """
    if not md_indices:
        return _parse_factor(term)

    head = ASTNode(Token("*", TType.Mul))
    i = 0
    md_index = -1
    while i < len(term):
        # first factor
        if md_index == -1:
            md_index = md_indices.pop(0)
            head.add_child(_parse_factor(term[i:md_index]))
            i = md_index + 1

        # remaining factors: have a * or / behind
        elif term[md_index].type() == TType.Div:
            """
            Express a/b as a(b)^-1
            """
            if not md_indices:
                head.add_child(inverse_factor(term[i:]))
                break

            md_index = md_indices.pop(0)
            head.add_child(inverse_factor(term[i:md_index]))
            i = md_index + 1

        elif term[md_index].type() == TType.Mul:
            if not md_indices:
                head.add_child(_parse_factor(term[i:]))
                break

            md_index = md_indices.pop(0)
            head.add_child(_parse_factor(term[i:md_index]))
            i = md_index + 1

    return head


def _parse_factor(factor: list[Token]) -> ASTNode:
    """Parse tokens on a factor and return its AST tree

    Args:
        factor (list[Token]): _description_

    Returns:
        ASTNode: head of the AST tree
    """
    if DEBUG:
        print("parse factor:", [token.literal() for token in factor])

    """    
    Case: factor := (expr)
    """
    if expr_inside_par(factor):
        return _parsetokens(factor)
    """    
    Case: factor is a function
    """
    if is_func(factor):
        return func_term(factor)
    """
    Case: factor is negative
    """
    if factor[0].type() == TType.Sub:
        return neg_term(factor[1:])

    if len(factor) == 1:
        if '.' in factor[0].literal():
            return frac_num(factor[0])

        return ASTNode(factor[0])

    """
    ranges of power expressions in the factor
    """
    pow_ranges = [
        {"start": (ran := powrange(factor, index))[0], "end": ran[1], "index": index}
        for (index, token) in enumerate(factor)
        if token.type() == TType.Pow and not token_inside_par(factor, index)
    ]

    if (
        len(pow_ranges) == 1
        and pow_ranges[0]["start"] == 0
        and pow_ranges[0]["end"] == len(factor) - 1
    ):
        return pow_factor(factor, pow_ranges[0])

    head = ASTNode(Token("*", TType.Mul))
    i = 0
    pow_range = None
    while i < len(factor):
        if pow_ranges and pow_range is None:
            pow_range = pow_ranges.pop(0)

        if pow_range is not None and i == pow_range["start"]:
            head.add_child(pow_factor(factor, range=pow_range))
            i = pow_range["end"] + 1
            pow_range = None

        elif token_is_func(factor[i]):
            end = find_closing_par(factor[i + 1 :])
            head.add_child(func_term(factor[i : end + 1]))
            i = end + 1

        elif factor[i].type() == TType.LPAR:
            end = find_closing_par(factor[i:])
            head.add_child(_parsetokens(factor[i : end + 1]))
            i = end + 1

        else:
            head.add_child(ASTNode(factor[i]) if '.' not in factor[i].literal() else frac_num(factor[i]))
            i += 1

    return head


def neg_term(term: list[Token]) -> ASTNode:
    """Produce an expression tree equivalent to: -term

    Args:
        term (list[Token]): tokenized term

    Returns:
        ASTNode: head of the AST tree
    """
    if DEBUG:
        print("neg term:", [token.literal() for token in term])

    head = ASTNode(Token("*", TType.Mul))
    head.add_child(ASTNode(Token("-1", TType.Num)))
    head.add_child(_parsetokens(term))
    return head


def pow_factor(expression: list[Token], range: dict[str, int]) -> ASTNode:
    """Produce the power tree of the factor in an expression located at (range[start], range[end])

    Args:
        factor (list[Token]): Tokenized expression
        range (dict[str, int]): range data: start, end, index (of power token)

    Returns:
        ASTNode: head of the power tree
    """
    if DEBUG:
        print("pow factor:", [token.literal() for token in expression])

    assert range.keys() == set(["start", "end", "index"])

    start = range["start"]
    pow_index = range["index"]
    end = range["end"]

    if DEBUG:
        print(f'base: {[token.literal() for token in expression[start:pow_index]]}') 
        print(f'power: {[token.literal() for token in expression[pow_index + 1 : end + 1]]}')


    head = ASTNode(expression[pow_index])
    head.add_child(_parsetokens(expression[start:pow_index]))
    head.add_child(_parsetokens(expression[pow_index + 1 : end + 1]))
    return head


def inverse_factor(factor: list[Token]) -> ASTNode:
    """Produce an expression tree equivalent to: 1/factor

    Args:
        factor (list[Token]): tokenized factor

    Returns:
        ASTNode: head of the AST tree
    """
    if DEBUG:
        print("inverse factor:", [token.literal() for token in factor])

    head = ASTNode(Token("^", TType.Pow))
    head.add_child(_parsetokens(factor))
    head.add_child(ASTNode(Token("-1", TType.Num)))
    return head


def func_term(term: list[Token]) -> ASTNode:
    """Produce the expression tree of the function term.
    Currently supports: sqrt, sin, cos, tan

    Args:
        term (list[Token]): Tokenized func term

    Returns:
        ASTNode: head of the AST tree
    """
    if DEBUG:
        print("func term:", [token.literal() for token in term])

    head = ASTNode(term[0])
    head.add_child(_parsetokens(term[1:]))
    return head


def frac_num(token: Token) -> ASTNode:
    """Produce the expression tree for a fraction derived from a decimal number

    Args:
        token (Token): Tokenized decimal number

    Returns:
        ASTNode: head of the frac AST tree
    """
    if DEBUG:
        print("frac term:", token.literal())

    num = token.literal().replace(".", "").lstrip("0")
    denom = str(10 ** (len(token.literal()) - 2))

    head = ASTNode(Token('frac', TType.Frac))
    head.add_child(ASTNode(Token(num, TType.Num)))
    head.add_child(ASTNode(Token(denom, TType.Num)))
    return head


def is_pm(token: Token) -> bool:
    return token.type() == TType.Add or token.type() == TType.Sub


def is_op(token: Token) -> bool:
    return (
        is_pm(token)
        or token.type() == TType.Mul
        or token.type() == TType.Div
        or token.type() == TType.Pow
        or token.type() == TType.Rem
    )


def token_is_func(token: Token) -> bool:
    """Check if a token is of func type

    Args:
        token (Token): Token object

    Returns:
        bool:
    """
    return (
        token.type() == TType.SIN
        or token.type() == TType.COS
        or token.type() == TType.TAN
        or token.type() == TType.SQRT
    )


def is_func(expression: list[Token]) -> bool:
    """Check if an _expression_ can be expanded as expression := func(expression)

    Args:
        expression (list[Token]): list of Token objects

    Returns:
        bool: _True_ if the expression is a function
    """
    if len(expression) <= 3:
        return False
    return token_is_func(expression[0]) and expr_inside_par(expression[1:])


def powrange(tokens: list[Token], pow_index: int) -> tuple[int, int]:
    """Returns the start and end index of a power expression in a token list

    Args:
        tokens (list[Token]): list of Token objects
        pow_index (int): index of the power ttype token in _tokens_

    Returns:
        tuple[int, int]: (_start_, _end_) indices of the power expression
    """
    start, end = pow_index - 1, pow_index + 1
    if tokens[end].type() == TType.LPAR:
        end = find_closing_par(tokens[end:])

    if tokens[start].type() == TType.RPAR:
        start = find_closing_par(tokens[:pow_index], reverse=True)
        if start - 1 >= 0 and is_func(tokens[start - 1 : pow_index]):
            start -= 1

    return start, end


def expr_inside_par(expression: list[Token]) -> bool:
    """Check if an _expression_ can be expanded as expression := (expression)

    Args:
        expression (list[Token]): list of Token objects

    Returns:
        bool: _True_ if the expression is enclosed in parentheses
    """
    return (
        expression[0].type() == TType.LPAR
        and find_closing_par(expression) == len(expression) - 1
    )


def token_inside_par(tokens: list[Token], index: int) -> bool:
    """Check if a token is surrounded by matching parentheses

    Args:
        tokens (list[Token]): list of Token objects
        index (int): index of Token object in list

    Returns:
        bool: _True_ if Token object is inside parenthesis
    """
    return count_par(tokens[index + 1 :]) != 0 and count_par(tokens[:index:-1]) != 0


def find_closing_par(tokens: list[Token], reverse: bool = False) -> int:
    """Find the index of the parenthesis matching the one at the beginning of the token list

    Args:
        tokens (list[Token]): list of Token objects

    Returns:
        int: index of the first parenthesis
    """
    p_count = 0
    step = -1 if reverse else 1
    for index, token in enumerate(tokens[::step]):
        if token.type() == TType.LPAR:
            p_count += 1
        elif token.type() == TType.RPAR:
            p_count -= 1

        if p_count == 0:
            return len(tokens) - index - 1 if reverse else index
    return -1


def count_par(tokens: list[Token]) -> int:
    """Returns 0 if the parenthesis tokens are balanced

    Args:
        tokens (list[Token]): list of Token objects

    Returns:
        int: 0 if balanced, the magnitude of the imbalance othewise
    """
    count = 0
    for token in tokens:
        if token.type() == TType.LPAR:
            count += 1
        if token.type() == TType.RPAR:
            count -= 1
    return count


def find_next_tok(tokens: list[Token], ttype: TType, greedy: bool = False) -> int:
    """Find the index of the next token of type **ttype**

    Args:
        tokens (list[Token]): list of Token objects
        ttype (TType): Token Type to be searched
        greedy (bool, optional): If true, returns the last token instance of ttype. Defaults to False.

    Returns:
        int: index of the found token
    """
    index = -1
    for i, token in enumerate(tokens):
        if token.type() == ttype:
            if not greedy:
                return i
            index = i

    return index
