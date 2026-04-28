[![wakatime](https://wakatime.com/badge/user/0b6c05fe-4823-446a-be83-4bd8575c84ab/project/ce19c349-a582-4cad-a3c6-274ea26d2889.svg)](https://wakatime.com/badge/user/0b6c05fe-4823-446a-be83-4bd8575c84ab/project/ce19c349-a582-4cad-a3c6-274ea26d2889)

# pyCAS
Mini Computer Algebra System using Python

## Features

- Mathematical expression parsing
- Variable substitution with a number or variable
- And soon(TM) more

## Examples

Create an Expression 

```python3
e = Expression.fromstr('3x+2')
print(e) # + ( * ( 3, x ), 2 )
```

Substitute the variable in an expression

```python3
f = subs(e, 'x', 5)
print(f) # + ( * ( 3, 5 ), 2 )
```

## Tests

Run all tests:

```bash
pyCas $ python -m unittest discover
```

Run tests from a specific file:

```bash
pyCas $ python -m unittest ./tests/filename.py
```