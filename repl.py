'''
repl.py

'''

from cas.parser import str_to_tokens
from cas.lexer import generate_expr

def get_line() -> str:
    return input("> ")

def main():
    line = get_line()
    while line != "exit":
        tokens = str_to_tokens(line)
        print('expr tree:', generate_expr(tokens).ops_to_string())
        line = get_line()

if __name__ == "__main__":
    main()