#!/usr/bin/env python3.6
'''
USAGE: ./tokenize.py <input.src

Compiles a toy language (see input.src) to Javascript,
which can be executed by piping into 'node'.

Destroy All Software, s07 0101 A compiler from scratch.
'''
from collections import namedtuple
import re
import sys

Token = namedtuple('Token', 'token_type value')

class Tokenizer:
    '''
    Splits given string into a sequence of Tokens.
    '''
    TOKEN_TYPES = [
        (r'\bdef\b',        'def'),
        (r'\bend\b',        'end'),
        (r'\b[a-zA-Z]+\b',  'identifier'),
        (r'\b[0-9]+\b',     'integer'),
        (r'\(',             'oparen'),
        (r'\)',             'cparen'),
        (r',',              'comma'),
    ]

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        while self.code:
            yield self.tokenize_one_token()

    def tokenize_one_token(self):
        for regex, token_type in Tokenizer.TOKEN_TYPES:
            match = re.match(regex, self.code)
            if match:
                value = match.group()
                self.code = self.code[len(value):].strip()
                return Token(token_type, value)
        raise RuntimeError(f"Couldn't match token on {self.code!r}")


def main(code):
    for token in Tokenizer(code).tokenize():
        print(token)

if __name__ == '__main__':
    main(sys.stdin.read())

