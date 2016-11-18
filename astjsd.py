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
import sys

SPACE = ' '
SYM = list(iter('()[]'))
# KEYWORD = ['rep','seq','alt','lit']

TOK = None # global variable

def mkseqno():
    n = 1000
    while 1:
        yield n
        n += 1
seqno = mkseqno()

def squeeze_blanks(s):
    pattern = r'[ ]+'
    replacement = ' '
    return re.sub(pattern, replacement, s)

def scan(inp):
    S = iter(squeeze_blanks(inp.replace('\n',' ') + '$'))
    t = S.next()
    while t != '$':
        if t == SPACE:
            t = S.next()
        elif t in SYM:
            yield t
            t = S.next()
        else: # keywords and literals, undistinguished
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
        self.sn = seqno.next()
    def set_label(self, literal):
        self.literal = literal
    def __repr__(self): return '(lit {})'.format(self.literal)
    def graph(self): return []
    def labels(self): return [(self.sn, self.literal)]
    def anno(self): return []

class Rep(object):
    def __init__(self):
        self.label = None
        self.child = []
        self.sn = seqno.next()
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
            n = (self.sn, c.sn)
            r.append(n)
        return r
    def labels(self):
        r = []
        for c in self.child:
            g = c.labels()
            r += g
        r.append((self.sn, self.label))
        return r
    def anno(self):
        r = []
        for c in self.child:
            g = c.anno()
            r += g
            n = (c.sn, 'rep')
            r.append(n)
        return r

class Seq(object):
    def __init__(self):
        self.label = None
        self.child = []
        self.sn = seqno.next()
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
            n = (self.sn, c.sn)
            r.append(n)
        return r
    def labels(self):
        r = []
        for c in self.child:
            g = c.labels()
            r += g
        r.append((self.sn, self.label))
        return r
    def anno(self):
        r = []
        for c in self.child:
            g = c.anno()
            r += g
            n = (c.sn, 'seq')
            r.append(n)
        return r

class Alt(object):
    def __init__(self):
        self.label = None
        self.child = []
        self.sn = seqno.next()
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
            n = (self.sn, c.sn)
            r.append(n)
        return r
    def labels(self):
        r = []
        for c in self.child:
            g = c.labels()
            r += g
        r.append((self.sn, self.label))
        return r
    def anno(self):
        r = []
        for c in self.child:
            g = c.anno()
            r += g
            n = (c.sn, 'alt')
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
    assert TOK == '(', repr(TOK)
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

def mkdot(target):
    target.send('digraph fig7 {\n')
    target.send('  node [shape=rect]\n')
    target.send('  edge [dir=none]\n')
    c = 1
    while 1:
        try:
            struct = (yield)
        except GeneratorExit:
            break
        g = struct.graph()
        n = struct.labels()
        a = dict(struct.anno())
        # Prefix 'cluster' alters layout behavior. Do not remove
        target.send('  subgraph cluster_compound%s {\n' % c)
        c += 1
        for (id, label) in n:
            try:
                kind = a[id]
            except KeyError:
                kind = 'root'
            if kind == 'rep':
                label = '*\\r' + label
            elif kind == 'alt':
                label = 'o\\r' + label
            target.send('    {} [label="{}"]\n'.format(id, label))
        for (parent, child) in g:
            target.send('    {} -> {}\n'.format(parent, child))
        target.send('  }\n')
    target.send('}\n')

def mkprinter():
    while 1:
        print (yield),

def clean_input(fh):
    return ''.join(m for m in fh.readlines() if not m.startswith('#'))

if __name__ == '__main__':
    printer = mkprinter()
    printer.next()
    dot = mkdot(printer)
    dot.next()
    inp = clean_input(sys.stdin)
    S = scan(inp)
    get()
    while TOK != '$':
        w = g()
        dot.send(w)
        get()
    dot.close()

# cat example/account.jsd |./astjsd.py |dot -T pdf >xxx.pdf ; evince xxx.pdf


