#!python

# TBD: add option show labels
# TBD: pretty print?
# TBD: the printer abstraction seems forced for this one-liner, expression language.

"""
Reduce ast to regex form. Only Lit labels are kept.
"""

import sys

def printer(out=sys.stdout):
    def aux():
        indent = 0
        while 1:
            try:
                cmd = (yield)
            except GeneratorExit:
                break
            if cmd == 'newline':
                print (file=out)
            else:
                spacer = ''
                print (spacer + cmd, end='', file=out)
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
                
def print_one(ast):
    p = printer()
    walk(p, ast)
    p.send('newline')
    
def print_many(ast):
    raise NotImplementedError
