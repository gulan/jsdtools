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

if 0:
    for rx in make_labeled_regexs():
        print (regex.asrepr(regex.parse_one(rx),False))
    
    for rx in texprs:
        print (regex.asrepr(regex.parse_one(rx),True))
    
    for rx in make_labeled_regexs():
        print (regex.asrepr(regex.parse_one(rx),True))

#  - - -  TESTS  - - -

def test_roundtrip_no_labels():
    for t in texprs:
        roundtrip(t, show_labels=False)
        
def test_roundtrip_with_labels():
    for t in make_labeled_regexs():
        roundtrip(t, show_labels=True)
    
