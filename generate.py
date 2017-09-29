#!/usr/bin/env python3.6
'''
USAGE: ./tokenize.py <input.src | ./parse.py | ./generate.py | node

Compiles a toy language (see input.src) to Javascript,
which can be executed by piping into 'node'.

Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
'''
import json
import sys
from textwrap import dedent

def generate(node):
    '''
    Generates Javascript for the given tree.
    '''
    if node['type_'] == 'def':
        return (
            'function {name}({arg_names}) '
            '{{ return {body} }};'.format(
                name=node['name'],
                arg_names=', '.join(node['arg_names']),
                body=generate(node['body']),
            )
        )
    elif node['type_'] == 'call':
        return (
            '{name}({arg_exprs})'.format(
                name=node['name'],
                arg_exprs=', '.join(map(generate, node['arg_exprs']))
            )
        )
    elif node['type_'] == 'var':
        return f'{node["name"]}'
    elif node['type_'] == 'int':
        return f'{node["value"]}'
    else:
        raise RuntimeError(
            f'Unexpected node type: {type(node).__name__} {node.value}')

def main(parse_tree):
    tree = json.loads(parse_tree)
    output = [generate(node) for node in tree]
    RUNTIME = [
        'function add(x, y) { return x + y };',
        'function print(x) { console.log(x) };',
    ]
    for line in RUNTIME + output:
        print(line)

if __name__ == '__main__':
    main(sys.stdin.read())

