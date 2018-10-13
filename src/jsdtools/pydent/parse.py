#!python

# TBD: code in jspre goes to render.

import sys

from itertools import count
from .. ast import (Rep, Alt, Lit, Seq)
from .scan import scan_one

class ParsingError(SyntaxError): pass

class Parser:

    def __init__(self):
        self.gensn = count(start=100)
    
    def parse(self, source):
        self.G = source
        self.token = self.next_token = None
        self.advance()
        return self.start()
    
    def advance(self):
        self.token, self.next_token = self.next_token, next(self.G, None)
	
    def accept(self, toktype):
        if self.next_token and self.next_token[0] == toktype:
            # print('accept>', self.next_token)
            self.advance()
            return True
        else:
            return False

    def expect(self, t):
        if not self.accept(t):
            raise ParsingError('Expected ' + t)

class PyformParser(Parser):
    """    
    tree := (lit | seq | alt | rep)
    seq := 'seq' . lit . ':' . indent . tree+ . dedent
    alt := 'alt' . lit . ':' . indent . tree+ . dedent
    rep := 'rep' . lit . ':' . indent . tree  . dedent
    """

    def start(self):
        return self.tree()
            
    def tree(self):
        if self.accept('lit'):
            ast = self.lit()
        elif self.accept('seq'):
            ast = self.seq()
        elif self.accept('alt'):
            ast = self.alt()
        else:
            self.expect('rep')
            ast = self.rep()
        return ast

    def lit(self):
        return Lit(self.token[1], next(self.gensn))
    
    def seq(self):
        self.advance()
        name = self.token[1]
        self.expect('colon')
        self.expect('indent')
        m = []
        while not self.accept('dedent'):
            ast = self.tree()
            m.append(ast)
        ast = Seq(name, next(self.gensn))
        for s in m:
            ast.add_child(s)
        return ast
    
    def alt(self):
        self.advance()
        name = self.token[1]
        self.expect('colon')
        self.expect('indent')
        m = []
        while not self.accept('dedent'):
            ast = self.tree()
            m.append(ast)
        ast = Alt(name, next(self.gensn))
        for s in m:
            ast.add_child(s)
        return ast
    
    def rep(self):
        self.advance()
        name = self.token[1]
        self.expect('colon')
        self.expect('indent')
        s = self.tree()
        self.expect('dedent')
        ast = Rep(name, next(self.gensn))
        ast.add_child(s)
        return ast

def parse_one(source=sys.stdin):
    tokens = scan_one(source=source)
    p = PyformParser()
    ast = p.parse(tokens)
    return ast

def parse_many(source=sys.stdin):
    raise NotIMplementedError

