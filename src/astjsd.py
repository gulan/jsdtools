#!python

# This module could renamed as 'lisp_to_x', but it will soon be
# obsoleted by jsp_syntax.

import argparse
import sys

import jsdtools.lisp as lisp
import jsdtools.dot as dot
import jsdtools.regex as regex

def dot_out(inp):
    ast_list = [ast for ast in lisp.parse_many(inp)]
    dot.print_many(*ast_list)

def regex_out(lines):
    m = [ast for ast in lisp.parse_many(lines)]
    for i in m:
        regex.print_one(i)


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
