#!python

# TBD: jsp_syntax will obsolete this script.

import argparse
import sys

from jsdtools.lisp import print_one
from jsdtools.pydent import parse_one

def display_lisp(source=sys.stdin):
    ast = parse_one(source)
    print_one(ast)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--syntax', default='lisp')
    args = parser.parse_args()
    if args.syntax == 'lisp':
        display_lisp()
    else:
        print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
        sys.exit(-1)
