#!python

# TBD: jsp_syntax will obsolete this script.

import argparse
import sys

import jsdtools.lisp as lisp
import jsdtools.pydent as pydent

def display_lisp(source=sys.stdin):
    ast = pydent.parse_one(source)
    lisp.print_one(ast)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--syntax', default='lisp')
    args = parser.parse_args()
    if args.syntax == 'lisp':
        display_lisp()
    else:
        print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
        sys.exit(-1)
