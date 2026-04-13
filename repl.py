'''
repl.py

REPL functionality:

expr_name : expression
Save an expression with the name expr_name

subs(expr_name, symbol = value)
Substitute the symbol in an expression with value

expr_name : pol(coefficients, symbol)
f : pol(3 2 1, x) -> 3x^2 + 2x + 1
'''

from cas import *
import regex as re

def get_line() -> str:
    return input("> ")

def main():
    expressions = dict() 
    line = get_line()
    while line != "exit":
        if (i := line.find(':')) > 0:
            expressions[line[:i].strip()] = Expression(line[i+1:].strip())
        elif line in expressions.keys():
            print(expressions[line])
        else:
            print('expr tree:', Expression(line))
        line = get_line()

if __name__ == "__main__":
    main()