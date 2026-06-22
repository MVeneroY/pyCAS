from functools import reduce
import operator

def gcd(n1: int, n2: int) -> int:
    if n1 == 0 or n2 == 0:
        return n1 + n2
    return gcd(n2, n1 % n2)


def lcd(n1: int, n2: int) -> int:
    return (n1 * n2) // gcd(n1, n2)


def ngcd(operands: list[int]) -> int:
    return reduce(gcd, operands)


def nlcd(operands: list[int]) -> int:
    return reduce(lcd, operands)