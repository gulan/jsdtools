#!python

"""
I have three different, but sematically equivalent syntaxes: lisp,
pydent and regex.

lisp: easy to parse, not so easy for people to read and edit. It is
the most direct serial form of the internal ast.

pydent: easy to read, write and edit. But uses indentation and
newlines, so an expression-like syntax cannot be used to write
one-liners.

regex: familiar, terse and great for getting started with a new
structure, but regexs quickly become unreadable for large trees.

This tool converts from any of these representations to any of the
others.

There is a fourth syntax: dot. But this one is a target syntax only. I
never try to parse it.

"""

import argparse
import sys

import jsdtools.lisp as lisp
import jsdtools.regex as regex
import jsdtools.pydent as pydent
import jsdtools.dot as dot

def translate(args):
    if args.syntaxin == 'pydent':
        p = pydent.parse_one
    elif args.syntaxin == 'lisp':
        p = lisp.parse_one
    elif args.syntaxin == 'regex':
        p = regex.parse_one
        
    if args.syntaxout == 'pydent':
        q = pydent.print_one
    elif args.syntaxout == 'lisp':
        q = lisp.print_one
    elif args.syntaxout == 'dot':
        q = dot.print_one
    elif args.syntaxout == 'regex':
        q = regex.print_one

    return lambda s: q(p(s))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--syntaxin', default='pydent')
    parser.add_argument('-z', '--syntaxout', default='lisp')
    args = parser.parse_args()
    
    if args.syntaxin not in ('pydent', 'lisp', 'regex'):
        print ("bad syntaxin option: %r" % args.syntaxin,
               file=sys.stderr)
        sys.exit(-1)
        
    if args.syntaxout not in ('pydent', 'lisp', 'regex', 'dot'):
        print ("bad syntaxout option: %r" % args.syntaxout,
               file=sys.stderr)
        sys.exit(-1)

    #  lisp scanner expects a string for any number of exprs
    #  regex scanner expects a string for any number of exprs
    #  pydent scanner expects iter for lines of a single file

    # newline is part of the syntax for pydent. The other formats
    # treat it as whitespace.
    
    tf = translate(args)
    if args.syntaxin == 'pydent':
        inp = sys.stdin
    else:
        inp = sys.stdin.read()
    tf(inp)
    sys.exit(0)
