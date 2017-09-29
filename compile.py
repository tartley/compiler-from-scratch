#!/usr/bin/env python3.6
'''
USAGE: ./compile.py <input.src | node

Compiles a toy language (see input.src) to Javascript,
which can be executed by piping into 'node'.

Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
'''
import sys
from textwrap import dedent

from tokenize import tokenize
from parse import Parser, DefNode, IntegerNode, CallNode, VarRefNode

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
                    arg_names=', '.join(node.arg_names),
                    body=self.generate(node.body),
                )
            )
        elif isinstance(node, CallNode):
            return (
                '{name}({arg_exprs})'.format(
                    name=node.name,
                    arg_exprs=', '.join(map(self.generate, node.arg_exprs))
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
    tokens = tokenize(code)
    tree = Parser(tokens).parse()
    generator = Generator()
    output = [generator.generate(node) for node in tree]
    RUNTIME = [
        'function add(x, y) { return x + y };',
        'function print(x) { console.log(x) };',
    ]
    for line in RUNTIME + output:
        print(line)

if __name__ == '__main__':
    main(sys.stdin.read())

