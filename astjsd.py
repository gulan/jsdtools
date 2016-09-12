#!/usr/bin/env python

"""
rep customers:
    seq onecust:
        invest
        alt movement:
            payin
            withdraw
        terminate
"""
f1 = """
(rep customer (
    seq onecust [
        (lit invest) 
        (alt movement [
            (lit payin)
            (lit withdraw)]) 
        (lit terminate)]))
"""
"""
G = '(' . X . ')'
X = REP | SEQ | ALT | LIT
REP = 'rep' . LABEL . G
SEQ = 'seq' . LABEL . '[' . G+ . ']'
ALT = 'alt' . LABEL . '[' . G+ . ']'
lit = 'lit' . LITERAL'
"""

import re
import StringIO
import runlen
import sys

SPACE = ' '
SYM = list(iter('()[]'))
KEYWORD = ['rep','seq','alt','lit']

TOK = None # global variable

def scan(inp):
    S = iter(runlen.runlen(inp.replace('\n',' ') + '$'))
    t = S.next()
    while t != '$':
        if t == SPACE:
            t = S.next()
        elif t in SYM:
            yield t
            t = S.next()
        else:
            word = ''
            while t != '$' and t not in SYM and t != SPACE:
                word += t
                t = S.next()
            yield word
    yield '$'

def get():
    global TOK
    TOK = S.next()
    # print >>sys.stderr, '   |TOK> {}'.format(TOK)

def expect(t):
    m = set(t)
    get()
    assert TOK in m, 'unexpected token: {}'.format(t)

# --- grammar-specific ---

class Lit(object):
    def __init__(self):
        self.child = None
        self.literal = None
    def set_label(self, literal):
        self.literal = literal
    def __repr__(self):
        return '(lit {})'.format(self.literal)
    def graph(self):
        return []
    def labels(self):
        return [(id(self), self.literal)]
    def anno(self):
        return []

class Rep(object):
    def __init__(self):
        self.label = None
        self.child = []
    def set_label(self, label):
        self.label = label
    def add_child(self, other):
        assert self.child == [], "rep allows only one child"
        self.child.append(other)
    def __repr__(self):
        return '(rep {} {})'.format(self.label,self.child[0])
    def graph(self):
        r = []
        for c in self.child:
            g = c.graph()
            r += g
            n = (id(self), id(c))
            r.append(n)
        return r
    def labels(self):
        r = []
        for c in self.child:
            g = c.labels()
            r += g
        r.append((id(self), self.label))
        return r
    def anno(self):
        r = []
        for c in self.child:
            g = c.anno()
            r += g
            n = (id(c), 'rep')
            r.append(n)
        return r

class Seq(object):
    def __init__(self):
        self.label = None
        self.child = []
    def set_label(self, label):
        self.label = label
    def add_child(self, other):
        self.child.append(other)
    def __repr__(self):
        cs = ' '.join(repr(c) for c in self.child)
        return '(seq {} [{}])'.format(self.label,cs)
    def graph(self):
        r = []
        for c in self.child:
            g = c.graph()
            r += g
            n = (id(self), id(c))
            r.append(n)
        return r
    def labels(self):
        r = []
        for c in self.child:
            g = c.labels()
            r += g
        r.append((id(self), self.label))
        return r
    def anno(self):
        r = []
        for c in self.child:
            g = c.anno()
            r += g
            n = (id(c), 'seq')
            r.append(n)
        return r

class Alt(object):
    def __init__(self):
        self.label = None
        self.child = []
    def set_label(self, label):
        self.label = label
    def add_child(self, other):
        self.child.append(other)
    def __repr__(self):
        cs = ' '.join(repr(c) for c in self.child)
        return '(alt {} [{}])'.format(self.label,cs)
    def graph(self):
        r = []
        for c in self.child:
            g = c.graph()
            r += g
            n = (id(self), id(c))
            r.append(n)
        return r
    def labels(self):
        r = []
        for c in self.child:
            g = c.labels()
            r += g
        r.append((id(self), self.label))
        return r
    def anno(self):
        r = []
        for c in self.child:
            g = c.anno()
            r += g
            n = (id(c), 'alt')
            r.append(n)
        return r

def lit():
    literal = TOK
    w = Lit()
    w.set_label(literal)
    return w

def rep():
    label = TOK
    w = Rep()
    w.set_label(label)
    get()
    r = g()
    w.add_child(r)
    return w

def seq():
    label = TOK
    w = Seq()
    w.set_label(label)
    expect('[')
    get()
    while TOK != ']':
        r = g()
        w.add_child(r)
        get()
    return w

def alt():
    label = TOK
    w = Alt()
    w.set_label(label)
    expect('[')
    get()
    assert TOK in set('(]')
    while TOK != ']':
        r = g()
        w.add_child(r)
        get()
    return w

def g():
    assert TOK == '('
    get()
    if TOK == 'rep':
        get()
        w = rep()
    elif TOK == 'seq':
        get()
        w = seq()
    elif TOK == 'alt':
        get()
        w = alt()
    elif TOK == 'lit':
        get()
        w = lit()
    expect(')')
    return w

def mkdot(struct):
    g = struct.graph()
    n = struct.labels()
    a = dict(struct.anno())
    yield 'digraph fig7 {\n'
    yield '  node [shape=rect]\n'
    yield '  edge [dir=none]\n'
    yield '  subgraph compound1 {\n'
    for (id, label) in n:
        try:
            kind = a[id]
        except KeyError:
            kind = 'root'
        if kind == 'rep':
            label = '*\\r' + label
        elif kind == 'alt':
            label = 'o\\r' + label
        yield '    {} [label="{}"]\n'.format(id, label)
    for (parent, child) in g:
        yield '    {} -> {}\n'.format(parent, child)
    yield '  }\n'
    yield '}\n'

if __name__ == '__main__':
    # cat customer.jsd |python astjsd.py |dot -T pdf >xxx.pdf ; evince xxx.pdf
    
    inp = ''.join(m for m in sys.stdin.readlines() if not m.startswith('#'))
    S = scan(inp)
    get()
    w = g()
    print '/* {} */'.format(repr(w))
    print
    for i in mkdot(w):
        print i,
    print

if 0:
    S = scan('(lit hello)')
    get(); w = g(); print w; print w.labels()
    S = scan('(seq abc [(lit hello)])')
    get(); w = g(); print w; print w.labels()
    S = scan('(seq abc [(lit hello) (lit goodbye)])')
    get(); w = g(); print w; print w.labels()
    S = scan('(seq abc [(lit hello) (seq def [(lit 1a) (lit 2a)]) (lit goodbye)])')
    get(); w = g(); print w; print w.labels()
    S = scan('(alt fruit [(lit apple) (lit banana) (lit cherry)])')
    get(); w = g(); print w; print w.labels()

if 0:
    D = '(lit D)'
    E = '(lit E)'
    F = '(lit F)'
    G = '(lit G)'
    B = '(seq B [{D} {E}])'.format(D=D, E=E)
    C = '(seq C [{F} {G}])'.format(F=F, G=G)
    A = '(seq A [{B} {C}])'.format(B=B, C=C)

if 0:
    S = scan(f1)
    get(); w = g(); print w
    print
    for i in mkdot(w):
        print i,
    print

if 0:
    print A
    S = scan(A)
    get(); w = g(); print w; print w.labels()
    S = scan(A)
    get(); w = g(); print w; print w.graph()

if 0:
    S = scan('(lit hello)')
    get(); w = g(); print w.graph()
    S = scan('(seq abc [(lit hello)])')
    get(); w = g(); print w.graph()
    S = scan('(seq abc [(lit hello) (lit goodbye)])')
    get(); w = g(); print w.graph()
    S = scan('(seq abc [(lit hello) (seq def [(lit 1a) (lit 2a)]) (lit goodbye)])')
    get(); w = g(); print w; print w.graph()
    S = scan('(alt fruit [(lit apple) (lit banana) (lit cherry)])')
    get(); w = g(); print w; print w.graph()

if 0:
    S = scan('(lit hello)')
    get(); w = g(); print w
    S = scan('(seq abc [(lit hello)])')
    get(); w = g(); print w
    S = scan('(seq abc [(lit hello) (lit goodbye)])')
    get(); w = g(); print w
    S = scan('(seq abc [(lit hello) (seq def [(lit 1a) (lit 2a)]) (lit goodbye)])')
    get(); w = g(); print w
    print '- '* 10
    S = scan('(alt fruit [(lit apple) (lit banana) (lit cherry)])')
    get(); w = g(); print w
    S = scan('(rep abc (lit hello))')
    get(); w = g(); print w
    print 'ok'
