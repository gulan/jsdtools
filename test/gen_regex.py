#!python

texprs = """(a|b|c|d|e|f)
(a|b)
(a|(b|(c|(d|(e|f)))))
(a|(b.c))
(a|(b*)|c)
(a|((b*)*)|c)
(a.b.c.d.e.f)
(a.b)
(a.(b|c))
(a.(b.(c.(d.(e.f)))))
(a.(b*).c)
(a.((b*)*).c)
(a*)
((a|b|c)|(d|e|f))
((a|b|c)*)
((a|b).c)
((a.b.c).(d.e.f))
((a.b.c)*)
((a.b)|c)
((a*)|b|c)
((a*)|(b*)|(c*))
((a*).b.c)
((a*).(b*).(c*))
((a*)*)
(((a|b)*)|c)
(((a|b)*)|(c*))
(((a.b)*).c)
(((a.b)*).(c*))
(((a*)*)|b|c)
(((a*)*)|((b*)*)|((c*)*))
(((a*)*).b.c)
(((a*)*).((b*)*).((c*)*))
((((a*)|b)*)|(c*))
((((a*).b)*).(c*))""".split('\n')

import jsdtools.dot as dot
import jsdtools.lisp as lisp
import jsdtools.pydent as pydent
import jsdtools.regex as regex

#  - - -  SUPPORT  - - -

def cannonical(rx, show_labels=False):
    return regex.asrepr(regex.parse_one(rx), show_labels)

def roundtrip(rx, show_labels=False):
    assert rx == cannonical(rx, show_labels), repr(rx)

def labels():
    chars = 'abkpxz'
    # Cartesian product:
    return (a+b+c for a in chars for b in chars for c in chars)

def insert_labels(rx):
    # A label may follow any ) character.
    
    # A label may also be used after a literal to rename it. That
    # feature seems to have little value, and is not tested here.
    g = labels()
    frags = rx.split(')')
    tmpl = '%s):%s'
    def asm(f): return (tmpl % (f,next(g)))
    m = ''.join(asm(f) for f in frags[:-1] ) + frags[-1]
    return m

def make_labeled_regexs():
    for t in texprs:
        yield insert_labels(t)

def gen_unlabled():
    for rx in make_labeled_regexs():
        yield (regex.asrepr(regex.parse_one(rx),False))

def gen_default_labeled():
    for rx in texprs:
        yield (regex.asrepr(regex.parse_one(rx),True))
    
def gen_synthetic_labeled():
    for rx in make_labeled_regexs():
        yield (regex.asrepr(regex.parse_one(rx),True))

def print_tests(form):
    # for r in gen_unlabled(): print (form % r)
    for r in gen_synthetic_labeled(): print (form % r)
    
def print_cmdline():
    for f in ('lisp', 'pydent', 'regex', 'dot'):
        form = 'echo \'%s\' |python ../src/jsp_syntax.py -y regex -z ' + f
        for r in gen_synthetic_labeled():
            print (form % r)

# print('from jsdtools import *')
print_cmdline()
# print_tests(form='pydent.print_one(regex.parse_one(%r))')
# print_tests(form='dot.print_one(regex.parse_one(%r))')
# print_tests(form='lisp.print_one(regex.parse_one(%r))')
# print_tests(form='regex.print_one(regex.parse_one(%r))')



