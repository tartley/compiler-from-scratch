#!/usr/bin/env python3.6
'''
USAGE: ./compiler.py <input.src | node

Compiles a toy language (see input.src) to Javascript,
which can be executed by piping into 'node'.

Destroy All Software, s07 0101 A compiler from scratch.
'''
from collections import namedtuple
import re
import sys
from textwrap import dedent

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


class Generator:
    '''
    Generates Javascript for the given tree.
    '''
    def generate(self, node):
        if isinstance(node, DefNode):
            return (
                'function {name}({arg_names}) '
                '{{ return {body} }};'.format(
                    name=node.name,
                    arg_names=','.join(node.arg_names),
                    body=self.generate(node.body),
                )
            )
        elif isinstance(node, CallNode):
            return (
                '{name}({arg_exprs})'.format(
                    name=node.name,
                    arg_exprs=','.join(map(self.generate, node.arg_exprs))
                )
            )
        elif isinstance(node, VarRefNode):
            return f'{node.value}'
        elif isinstance(node, IntegerNode):
            return f'{node.value}'
        else:
            raise RuntimeError(
                f'Unexpected node type: {type(node).__name__} {node.value}')


def main(code):
    tokens = Tokenizer(code).tokenize()
    tree = Parser(tokens).parse()
    generator = Generator()
    output = [generator.generate(node) for node in tree]
    # output a runtime
    print(dedent('''\
        function add(x, y) { return x + y };
        function print(x) { console.log(x) };
    '''))
    # output code for our parsed input
    for line in output:
        print(line)
    # if output is piped into node, expect result '123'


if __name__ == '__main__':
    main(sys.stdin.read())

