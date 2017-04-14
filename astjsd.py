#!/usr/bin/env python

# The way I usually write it.
"""
rep customers:
    seq onecust:
        invest
        alt movement:
            payin
            withdraw
        terminate
"""

# The lisp-like syntax used here.
# (Store in file named account.jsd)
"""
(rep customer (
    seq onecust [
        (lit invest) 
        (alt movement [
            (lit payin)
            (lit withdraw)]) 
        (lit terminate)]))
"""

# Meta Syntax
"""
      G = '(' . X . ')'
      X = REP | SEQ | ALT | LIT
    REP = 'rep' . LABEL . G
    REP1 = 'rep+' . LABEL . G
    SEQ = 'seq' . LABEL . '[' . G+ . ']'
    ALT = 'alt' . LABEL . '[' . G+ . ']'
    LIT = 'lit' . LITERAL'
"""

import re
import sys

PUNCT = list(iter('()[]'))
TOK = None # global variable

def mkseqno():
    n = 1000
    while 1:
        yield n
        n += 1
seqno = mkseqno()

def scan(inp):
    # convert inp string to sequence of tokens
    def squeeze_blanks(s):
        pattern = r'[ ]+'
        replacement = ' '
        return re.sub(pattern, replacement, s)

    K = iter(squeeze_blanks(inp.replace('\n',' ') + '$'))
    t = K.next()
    while t != '$':
        if t == ' ':
            t = K.next()
        elif t in PUNCT:
            yield t
            t = K.next()
        else: # keywords and literals, undistinguished
            word = ''
            while t != '$' and t not in PUNCT and t != ' ':
                word += t
                t = K.next()
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

class Abstract(object):
    def __init__(self,label):
        self.child = []
        self.label = label
        self.ntype = self.__class__.__name__.lower()
        self.sn = seqno.next()

    def __repr__(self): raise NotImplemented

    def anno(self):
        """The compound nodes (alt and rep) are shown on the output
        tree by marks (* or o) on their child nodes. The anno method
        builds a map from each node's unique sn to the type ('alt',
        'rep') of its parent."""
        raise NotImplemented

    def graph(self):
        """ Returns a list of parent-child pairs. Only the sequence
        number is given for each node.  """
        raise NotImplemented

    def labels(self):
        """A label is the user-given name of a node. Note that the
        name may be any string that the user provides, and is not
        resticted to looking like an identifier.

        This function returns a list of node-label pairs. Each node is
        by it sequence number"""
        raise NotImplemented

class Lit(Abstract):
    def __repr__(self): return '({} {})'.format(self.ntype,self.label)
    def graph(self): return []
    def labels(self): return [(self.sn, self.label)]
    def anno(self): return []

class Compound(Abstract):
    def __repr__(self): return '({} {} {})'.format(self.ntype,self.label,self.children())
    def add_child(self, other): self.child.append(other)

    def anno(self):
        r = []
        for c in self.child:
            r += c.anno()
            r.append((c.sn, self.ntype))
        return r

    def graph(self):
        r = []
        for c in self.child:
            r += c.graph()
            r.append((self.sn, c.sn))
        return r

    def labels(self):
        r = []
        for c in self.child:
            r += c.labels()
            r.append((self.sn, self.label))
        return r

class Rep(Compound):
    def add_child(self, other):
        assert self.child == [], "rep allows only one child"
        Compound.add_child(self,other)
    def children(self): return self.child[0]

class Rep1(Compound):
    def add_child(self, other):
        assert self.child == [], "rep allows only one child"
        Compound.add_child(self,other)
    def children(self): return self.child[0]

class Seq(Compound):
    def children(self): return ' '.join(repr(c) for c in self.child)

class Alt(Compound):
    def children(self): return ' '.join(repr(c) for c in self.child)

def lit():
    return Lit(TOK)

def rep():
    w = Rep(TOK)
    get()
    w.add_child(g())
    return w

def rep1():
    w = Rep1(TOK)
    get()
    w.add_child(g())
    return w

def seq():
    w = Seq(TOK)
    expect('[')
    get()
    while TOK != ']':
        w.add_child(g())
        get()
    return w

def alt():
    w = Alt(TOK)
    expect('[')
    get()
    assert TOK in set('(]')
    while TOK != ']':
        w.add_child(g())
        get()
    return w

def g():
    assert TOK == '(', repr(TOK)
    get()
    if TOK == 'rep':
        get(); w = rep()
    elif TOK == 'rep1':
        get(); w = rep1()
    elif TOK == 'seq':
        get(); w = seq()
    elif TOK == 'alt':
        get(); w = alt()
    elif TOK == 'lit':
        get(); w = lit()
    expect(')')
    return w

def mkdot(target):
    def _aux():
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
                    ntype = a[id]
                except KeyError:
                    ntype = 'root'
                if ntype == 'rep':
                    label = '*\\r' + label
                elif ntype == 'rep1':
                    label = '+\\r' + label
                elif ntype == 'alt':
                    label = 'o\\r' + label
                target.send('    {} [label="{}"]\n'.format(id, label))
            for (parent, child) in g:
                target.send('    {} -> {}\n'.format(parent, child))
            target.send('  }\n')
        target.send('}\n')
    x = _aux()
    x.next()
    return x

def mkprinter():
    def _aux():
        while 1:
            print (yield),
    printer = _aux()
    printer.next()
    return printer

def filter_comments(fh):
    return ''.join(m for m in fh.readlines()
                   if not m.startswith('#') and not m.startswith(';'))

if __name__ == '__main__':
    dot = mkdot(mkprinter())
    S = scan(filter_comments(sys.stdin)) # S is a global in get()
    get()
    while TOK != '$': # TOK is a global set by get()
        w = g()
        dot.send(w)
        get()
    dot.close()

# cat example/account.jsd |./astjsd.py |dot -T pdf >xxx.pdf ; evince xxx.pdf


