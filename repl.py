'''
repl.py

'''

from cas import get_tokens, expr

def get_line() -> str:
    return input("> ")

def main():
    line = get_line()
    while line != "exit":
        print('expr tree:', expr(get_tokens(line)).ops_to_string())
        line = get_line()

if __name__ == "__main__":
    main()