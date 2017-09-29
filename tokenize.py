#!/usr/bin/env python3.6
'''
First stage (tokenize) for a three-stage compiler.

USAGE: ./tokenize.py [-h] <input.src | ./parse.py | ./generate.py | node

    -h   Format the JSON output with human-readable indentation

Given source code of a toy language on stdin (see input.src),
produces a sequence of tokens as JSON on stdout,
which can be piped into ./parse.py.
'''
from collections import namedtuple
import json
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

class Tokenize:

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        '''
        Splits given string into a sequence of Tokens.
        '''
        while self.code:
            yield self.tokenize_one_token()

    def tokenize_one_token(self):
        for regex, token_type in TOKEN_TYPES:
            match = re.match(regex, self.code)
            if match:
                value = match.group()
                self.code = self.code[len(value):].strip()
                return Token(token_type, value)
        raise RuntimeError(f"Couldn't match token on {code!r}")

def main(code):
    indent = 4 if '-h' in sys.argv else None
    tokenizer = Tokenize(code)
    print(json.dumps(list(tokenizer.tokenize()), indent=indent))

if __name__ == '__main__':
    main(sys.stdin.read())

