#!/usr/bin/env python3.6
'''
Third stage (Code generation) for a three-stage compiler.

USAGE: ./tokenize.py <input.src | ./parse.py | ./generate.py | node

Given a parsed node tree as JSON on stdin,
generates equivalent Javascript on stdout,
which can be executed by piping into 'node'.
'''
import json
import sys
from textwrap import dedent

def generate(node):
    '''
    Generates Javascript for the given tree.
    '''
    if node['node_type'] == 'def':
        return (
            'function {name}({arg_names}) '
            '{{ return {body} }};'.format(
                name=node['name'],
                arg_names=', '.join(node['arg_names']),
                body=generate(node['body']),
            )
        )
    elif node['node_type'] == 'call':
        return (
            '{name}({arg_exprs})'.format(
                name=node['name'],
                arg_exprs=', '.join(map(generate, node['arg_exprs']))
            )
        )
    elif node['node_type'] == 'var':
        return f'{node["name"]}'
    elif node['node_type'] == 'int':
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

