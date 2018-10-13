#!python

# History: This was the first concrete syntax that I wrote. Parsing it
# was a bit easier than the indent style that I prefer. Now that I
# also have an indent style parser, I keep this syntax as the
# canonical form as it makes a good concrete representation of the AST.

# TBD: The style of this code should be updated to look like the other
# parser/scanners.

# TBD: I will likely drop rep1.

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

from .. ast import (Rep, Rep1, Alt, Lit, Seq)
from .scan import scan_one

class ParsingException(Exception): pass

class Parser:

    def __init__(self, source):
        self.G = source         # stream of tokens
        self.TOK = None

    def get(self):
        self.TOK = next(self.G)

    def expect(self, t):
        # TBD: Too general as t is always a single character.
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
        if self.TOK != '(':
            raise ParsingException(self.TOK)
        # assert self.TOK == '(', repr(self.TOK)
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

def parse_one(inp):
    tokens = scan_one(inp)
    p = Parser(tokens)
    p.get()
    return p.parse()

def parse_many(inp):
    tokens = scan_one(inp)
    p = Parser(tokens)
    p.get()
    while p.TOK != '$':
        yield p.parse()
        p.get()
