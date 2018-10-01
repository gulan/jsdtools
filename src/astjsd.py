#!python

# This module could renamed as 'lisp_to_x', but it will soon be
# obsoleted by jsp_syntax.

import argparse
import sys

from jsdtools.lisp import parse_many
import jsdtools.dot as dot
from jsdtools.regex import print_one

def dot_out(inp):
    ast_list = [ast for ast in parse_many(inp)]
    dot.print_many(*ast_list)

def regex_out(lines):
    m = [ast for ast in parse_many(lines)]
    for i in m:
        print_one(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--syntax', default='dot')
    args = parser.parse_args()
    if args.syntax == 'dot':
        lines = sys.stdin.readlines()
        dot_out(lines)
    elif args.syntax == 'regex':
        lines = sys.stdin.readlines()
        regex_out(lines)
    else:
        print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
        sys.exit(-1)
    

# cat example/account/account.jsd |./astjsd.py |dot -T pdf >/tmp/account.pdf ; evince /tmp/account.pdf
