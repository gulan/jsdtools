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

import jsdtools.ast as ast
import jsdtools.dot as dot
import jsdtools.lisp as lisp
import jsdtools.pydent as pydent
import jsdtools.regex as regex

def cannonical(rx, show_labels=False):
    return regex.asrepr(regex.parse_one(rx), show_labels)

def roundtrip(rx, show_labels=False):
    assert rx == cannonical(rx, show_labels), repr(rx)

def labels():
    chars = 'abkpxz'
    return (a+b+c for a in chars for b in chars for c in chars)

g = labels()

def insert_labels(rx):
    frags = rx.split(')')
    tmpl = '%s):%s'
    def asm(f): return (tmpl % (f,next(g)))
    m = ''.join(asm(f) for f in frags[:-1] ) + frags[-1]
    return m

def make_labeled_regexs():
    for t in texprs:
        yield insert_labels(t)

def test_roundtrip_no_labels():
    for t in texprs:
        roundtrip(t, show_labels=False)
        
def test_roundtrip_with_labels():
    for t in make_labeled_regexs():
        roundtrip(t, show_labels=True)

if 0:
    for rx in make_labeled_regexs():
        print (regex.asrepr(regex.parse_one(rx),False))
    
    for rx in texprs:
        print (regex.asrepr(regex.parse_one(rx),True))
    
    for rx in make_labeled_regexs():
        print (regex.asrepr(regex.parse_one(rx),True))
    
