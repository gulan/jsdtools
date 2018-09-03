#!python

import argparse
import sys
from jsdtools.lisp_syntax.parse_lisp import parse_many
from jsdtools.dot_syntax.render_dot import mkdot, mkprinter
from jsdtools.regex_syntax.render_re import print_ast

def dot_out(inp):
    dot = mkdot(mkprinter())
    for ast in parse_many(inp):
        dot.send(ast)
    dot.close()

def regex_out(lines):
    m = [ast for ast in parse_many(lines)]
    for i in m:
        print_ast(i)


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


