#!python

"""
Serialize the ast to the lisp-like form of jsp.

"""

import sys
# from parse_lisplike_jsp import Scanner, Parser

def printer():
    def aux():
        indent = 0
        while 1:
            try:
                cmd = (yield)
            except GeneratorExit:
                break
            if cmd == 'indent':
                indent += 1
            elif cmd == 'dedent':
                indent -= 1
            elif cmd == 'newline':
                print ()
            else:
                spacer = ' ' * indent
                print (spacer+cmd, end='')
    g = aux()
    next(g)
    return g

def walk(printer, ast, level=0):
    if ast.ntype == 'lit':
        s = '(lit %s' % ast.label
    elif ast.ntype == 'seq':
        s = '(seq %s [' % ast.label
    elif ast.ntype == 'alt':
        s = '(alt %s [' % ast.label
    elif ast.ntype == 'rep':
        s = '(rep %s' % ast.label
        
    printer.send(s)
    if ast.ntype != 'lit':
        printer.send('newline')
    
    for ch in ast.child:
        printer.send('indent')
        walk(printer, ch, level=level+1)
        printer.send('dedent')
        
    if ast.ntype == 'lit':
        s = ')'
    elif ast.ntype == 'seq':
        s = '])'
    elif ast.ntype == 'alt':
        s = '])'
    elif ast.ntype == 'rep':
        s = ')'

    printer.send(s)
    printer.send('newline')


# def main(data):
#     t = Parser(Scanner(data))
#     t.get()
#     ast = t.parse()
#     p = printer()
#     walk(p, ast)
        

# if __name__ == '__main__':
#     main(sys.stdin.readlines())
