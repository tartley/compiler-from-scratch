#!/usr/bin/env python3.6
'''
USAGE: ./tokenize.py <input.src | ./parse.py [-h]

    -h   Format the JSON output with human-readable indentation

Compiles a toy language (see input.src) to Javascript,
which can be executed by piping into 'node'.

Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
'''
from collections import namedtuple
import json
import sys

from tokenize import Token

DefNode = namedtuple('DefNode', 'name arg_names body')
IntegerNode = namedtuple('IntegerNode', 'value')
CallNode = namedtuple('CallNode', 'name arg_exprs')
VarRefNode = namedtuple('VarRefNode', 'value')

class Parser:
    '''
    Parse sequence of tokens into a grammar tree.
    '''
    def __init__(self, tokens):
        self.tokens = list(tokens)

    def parse(self):
        while self.tokens:
            if self.peek('def'):
                yield self.parse_def()
            else:
                yield self.parse_call()

    def consume(self, expected_type):
        token = self.tokens.pop(0)
        if token.token_type == expected_type:
            return token
        else:
            raise RuntimeError(
                f"Expected token type {expected_type!r} "
                f"but got {token.token_type!r}."
            )

    def peek(self, expected_type, offset=0):
        return self.tokens[offset].token_type == expected_type

    def parse_def(self):
        self.consume('def')
        name = self.consume('identifier').value
        arg_names = list(self.parse_arg_names())
        body = self.parse_expr()
        self.consume('end')
        return dict(
            type_='def',
            name=name,
            arg_names=arg_names,
            body=body,
        )

    def parse_arg_names(self):
        self.consume('oparen')
        if self.peek('identifier'):
            yield self.consume('identifier').value
            while self.peek('comma'):
                self.consume('comma')
                yield self.consume('identifier').value
        self.consume('cparen')

    def parse_expr(self):
        if self.peek('integer'):
            return self.parse_integer()
        elif self.peek('identifier') and self.peek('oparen', 1):
            return self.parse_call()
        else:
            return self.parse_var_ref()

    def parse_call(self):
        name = self.consume('identifier').value
        arg_exprs = list(self.parse_arg_exprs())
        return dict(
            type_='call',
            name=name,
            arg_exprs=arg_exprs,\
        )

    def parse_arg_exprs(self):
        self.consume('oparen')
        if not self.peek('cparen'):
            yield self.parse_expr()
            while self.peek('comma'):
                self.consume('comma')
                yield self.parse_expr()
        self.consume('cparen')

    def parse_integer(self):
        return dict(
            type_='int',
            value=int(self.consume('integer').value),
        )

    def parse_var_ref(self):
        return dict(
            type_='var',
            name=self.consume('identifier').value,
        )

def main(serialized_tokens):
    tokens = [Token(*token) for token in json.loads(serialized_tokens)]
    tree = Parser(tokens).parse()
    indent = 4 if '-h' in sys.argv else None
    print(json.dumps(list(tree), indent=indent))

if __name__ == '__main__':
    main(sys.stdin.read())

