#!/usr/bin/env python3.6
'''
USAGE: ./compiler.py <input.src | node

Compiles a toy language (see input.src) to Javascript,
which can be executed by piping into 'node'.

Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
'''
from collections import namedtuple
import sys

from tokenize import tokenize

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

    def parse(self):
        while self.tokens:
            if self.peek('def'):
                yield self.parse_def()
            else:
                yield self.parse_call()

    def parse_def(self):
        self.consume('def')
        name = self.consume('identifier').value
        arg_names = list(self.parse_arg_names())
        body = self.parse_expr()
        self.consume('end')
        return DefNode(name, arg_names, body)

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
        n = CallNode(name, arg_exprs)
        return n

    def parse_arg_exprs(self):
        self.consume('oparen')
        if not self.peek('cparen'):
            yield self.parse_expr()
            while self.peek('comma'):
                self.consume('comma')
                yield self.parse_expr()
        self.consume('cparen')

    def parse_integer(self):
        return IntegerNode(int(self.consume('integer').value))

    def parse_var_ref(self):
        return VarRefNode(self.consume('identifier').value)

def main(code):
    tokens = tokenize(code)
    tree = Parser(tokens).parse()
    for node in tree:
        print(node)

if __name__ == '__main__':
    main(sys.stdin.read())

