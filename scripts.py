# from cas._parser import gen_factor
from cas.lexer import gettokens
# from cas._parser_balance import _parsetokens, _parse_term, _parse_factor
from cas.expression import Expression
from cas.engine import subs

# s = 'cos(23)^7x^2y^2(x*5)^3'
s = '21+4 - cos(5)'
# print([token.literal() for token in s])
h = Expression.fromstr(s)
print(h)
print(h._syms)
h2 = subs(h, 'x', '3')
print(h2)
print(h2._syms)