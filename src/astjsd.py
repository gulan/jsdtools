#!python

# Lang extension to give coorsp.

import sys
from jsdtools.lisp_syntax.parse_lisp import Scanner, Parser
from jsdtools.dot_syntax.render_dot import mkdot, mkprinter

def main(data):
    dot = mkdot(mkprinter())
    t = Parser(Scanner(data))
    t.get()
    while t.TOK != '$':
        ast = t.parse()
        dot.send(ast)
        t.get()
    dot.close()
    

if __name__ == '__main__':
    main(sys.stdin.readlines())

# cat account/account.jsd |./astjsd.py |dot -T pdf >/tmp/account.pdf ; evince /tmp/account.pdf

