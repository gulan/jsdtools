#!python

"""
Reduce ast to regex form. Only Lit labels are kept.
"""

import sys

def printer():
    def aux():
        indent = 0
        while 1:
            try:
                cmd = (yield)
            except GeneratorExit:
                break
            if cmd == 'newline':
                print ()
            else:
                spacer = ''
                print (spacer + cmd, end='')
    g = aux()
    next(g)
    return g

def walk(printer, ast):
    if ast.ntype == 'lit':
        s = '%s' % ast.label
        printer.send(s)
        
    elif ast.ntype == 'seq':
        children = iter(ast.child)
        printer.send('(')
        first = next(children)
        walk(printer, first)
        for ch in children:
            printer.send(' . ')
            walk(printer, ch)
        printer.send(')')
        
    elif ast.ntype == 'alt':
        children = iter(ast.child)
        printer.send('(')
        first = next(children)
        walk(printer, first)
        for ch in children:
            printer.send(' | ')
            walk(printer, ch)
        printer.send(')')
        
    elif ast.ntype == 'rep':
        first = ast.child[0]
        walk(printer, first)
        printer.send('*')
                
def print_ast(ast):
    p = printer()
    walk(p, ast)
    p.send('newline')
