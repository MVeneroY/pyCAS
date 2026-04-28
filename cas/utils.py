from cas.expression import Expression


def poly(coefficients: list[str] | list[int], symbol: str) -> Expression:
    """Create a single variable polynomial expression given a list of coefficients

    Args:
        coefficients (list[str] | list[int]): List of coefficents, starting from the leading coefficients
        symbol (str): coefficient symbol

    Returns:
        Expression: Expression object

    Example:
        poly([5,0,-4]) -> 5x^2 - 4
    """
    try:
        assert len(coefficients) > 0
    except:
        raise Exception(f"list {coefficients = } is empty")
    string = ""
    for i, c in enumerate(coefficients):
        if type(c) == int:
            string += str(c) + "x^" + str(len(coefficients) - i - 1) + "+"
        else:
            string += c + "x^" + str(len(coefficients) - i - 1) + "+"

    return Expression.fromstr(string)
