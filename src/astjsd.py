#!python

# This module could renamed as 'lisp_to_x', but it will soon be
# obsoleted by jsp_syntax.

import argparse
import sys

import jsdtools.lisp as lisp
import jsdtools.dot as dot
import jsdtools.regex as regex

def dot_out(text):
    ast_list = list(lisp.parse_many(text))
    dot.print_many(*ast_list)

def regex_out(text):
    for i in lisp.parse_many(text):
        regex.print_one(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--syntax', default='dot')
    args = parser.parse_args()
    if args.syntax == 'dot':
        text = sys.stdin.read()
        dot_out(text)
    elif args.syntax == 'regex':
        text = sys.stdin.read()
        regex_out(text)
    else:
        print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
        sys.exit(-1)
    sys.exit(0)
    

# python astjsd.py -y dot   <../example/all.jsd
# python astjsd.py -y regex <../example/all.jsd

# |dot -T pdf >all.pdf ; evince all.pdf
