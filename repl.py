'''
repl.py

'''

from parser import str_to_tokens

def get_line() -> str:
    return input("> ")

def main():
    line = get_line()
    while line != "exit":
        print(str_to_tokens(line))
        line = get_line()

if __name__ == "__main__":
    main()