#!/usr/bin/env python3.6
'''
USAGE: ./tokenize.py <input.src

Compiles a toy language (see input.src) to Javascript,
which can be executed by piping into 'node'.

Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
'''
from collections import namedtuple
import re
import sys

Token = namedtuple('Token', 'token_type value')

TOKEN_TYPES = [
    (r'\bdef\b',        'def'),
    (r'\bend\b',        'end'),
    (r'\b[a-zA-Z]+\b',  'identifier'),
    (r'\b[0-9]+\b',     'integer'),
    (r'\(',             'oparen'),
    (r'\)',             'cparen'),
    (r',',              'comma'),
]

def tokenize(code):
    '''
    Splits given string into a sequence of Tokens.
    '''
    while code:
        token, code = tokenize_one_token(code)
        yield token

def tokenize_one_token(code):
    for regex, token_type in TOKEN_TYPES:
        match = re.match(regex, code)
        if match:
            value = match.group()
            code = code[len(value):].strip()
            return Token(token_type, value), code
    raise RuntimeError(f"Couldn't match token on {code!r}")

def main(code):
    for token in tokenize(code):
        print(token)

if __name__ == '__main__':
    main(sys.stdin.read())

