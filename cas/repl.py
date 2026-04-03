'''
repl.py

'''

from cas.parser import str_to_tokens
from cas.lexer import tokens_to_nodes

def get_line() -> str:
    return input("> ")

def main():
    line = get_line()
    while line != "exit":
        tokens = str_to_tokens(line)
        print('tokens:', tokens)
        print('nodes:', tokens_to_nodes(tokens))
        line = get_line()

if __name__ == "__main__":
    main()