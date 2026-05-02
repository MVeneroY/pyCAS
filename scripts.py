# from cas._parser import gen_factor
from cas.lexer import gettokens
from cas.parser import frac_num
# from cas._parser_balance import _parsetokens, _parse_term, _parse_factor
from cas.expression import Expression
from cas.engine import _frac_add, _simplify_frac, _simplifymul
from cas.utils import poly

f1 = Expression.fromstr('2 * 5 / 3')
print(f1)
f2 = Expression(
    _simplifymul(f1._expression)
)
print(f2)