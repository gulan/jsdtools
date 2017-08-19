#!/usr/bin/python

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

from abstract_jsp_ast import Rep, Rep1, Alt, Lit, Seq
import re

def Scanner(inp):
    # Convert `inp` string to sequence of tokens
    PUNCT = list(iter('()[]'))
    
    def filter_comments(text):
        return ''.join(m for m in text
                       if not m.startswith('#') and not m.startswith(';'))

    def squeeze_blanks(s):
        s = s.replace('\t',' ')
        s = s.replace('\n',' ')
        return re.sub(r'[ ]+', ' ', s) # leave a space
    
    K = iter(squeeze_blanks(filter_comments(inp) + '$'))
    
    t = K.next()
    while t != '$': # the $ is my made-up end-of-string.
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

class Parser(object):

    def __init__(self, source):
        self.G = source
        self.TOK = None

    def get(self):
        self.TOK = self.G.next()

    def expect(self, t):
        m = set(t)
        self.get()
        assert self.TOK in m, 'unexpected token: {}'.format(t)

    def lit(self): return Lit(self.TOK)

    def rep(self):
        w = Rep(self.TOK)
        self.get()
        w.add_child(self.parse())
        return w

    def rep1(self):
        w = Rep1(self.TOK)
        self.get()
        w.add_child(self.parse())
        return w

    def seq(self):
        w = Seq(self.TOK)
        self.expect('[')
        self.get()
        while self.TOK != ']':
            w.add_child(self.parse())
            self.get()
        return w

    def alt(self):
        w = Alt(self.TOK)
        self.expect('[')
        self.get()
        assert self.TOK in set('(]'), "TOK=%r" % self.TOK
        while self.TOK != ']':
            w.add_child(self.parse())
            self.get()
        return w

    def parse(self):
        assert self.TOK == '(', repr(self.TOK)
        self.get()
        d = {'rep': self.rep,
             'rep1': self.rep1,
             'seq': self.seq,
             'alt': self.alt,
             'lit': self.lit}
        func = d.get(self.TOK)
        assert func
        self.get()
        w = func()
        self.expect(')')
        return w
