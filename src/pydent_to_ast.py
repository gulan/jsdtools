#!python

import argparse
import sys
from jsdtools.lisp.render import print_ast
from jsdtools.pydent.parse import parse_one

def display_lisp(source=sys.stdin):
    ast = parse_one(source)
    print_ast(ast)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--syntax', default='lisp')
    args = parser.parse_args()
    if args.syntax == 'tree':
        pass
    elif args.syntax == 'lisp':
        display_lisp()
    elif args.syntax == 'dot':
        pass
    else:
        print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
        sys.exit(-1)
