from cas import get_tokens, expr
from cas.expression import Expression
from cas.engine import substitute, evaluate

s = Expression('3x^2 + 16x +4')
print(s)

s = substitute(s, 'x', '2')
print(evaluate(s))