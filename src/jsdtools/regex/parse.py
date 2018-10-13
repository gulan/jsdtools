#!python

# TBD: take Scanner invocation out of Parser

from itertools import (count, cycle)
from .. ast import (Rep, Alt, Lit, Seq)
from . scan import (Scanner, ScanError)

class ParsingError(Exception): pass

class Parser:

    def parse(self, source, test_counter = False):
        # print('------------  %s  ------------' % source)
        self.G = Scanner(source)
        self.token = self.next_token = None
        self.advance()
        if test_counter:
            self.count = cycle([0])
        else:
            self.count = count(start=1)
        return self.start()
    
    def name(self):
        return "_%d" % next(self.count)
    
    def advance(self):
        try:
            self.token, self.next_token = self.next_token, next(self.G, None)
        except ScanError as e:
            raise ParsingError(e)
	
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

class RegexParser(Parser):
    """    
    alt = seq ('|' seq)*
    seq = rep ('.' rep)*
    rep = trm ('*')*
    trm = exp [':' lit]
    exp = lit | sub
    sub = '(' alt ')'
    """

    def start(self):
        return self.alt()
    
    def alt(self):
        m = []
        first = ast = self.seq()
        m.append(ast)
        while self.accept('bar'):
            ast = self.seq()
            m.append(ast)
        if len(m) > 1:
            n = Alt(self.name())
            for i in m:
                n.add_child(i)
            return n
        else:
            return first
    
    def seq(self):
        m = []
        first = ast = self.rep()
        m.append(ast)
        while self.accept('dot'):
            ast = self.rep()
            m.append(ast)
        if len(m) > 1:
            n = Seq(self.name())
            for i in m:
                n.add_child(i)
            return n
        else:
            return first
        
    def rep(self):
        ast = self.trm()
        while self.accept('star'):
            ast1 = Rep(self.name())
            ast1.add_child(ast)
            ast = ast1
        return ast
        
    def trm(self):
        ast = self.exp()
        if self.accept('colon'):
            self.advance()
            label = self.token[1]
            ast.label = label
        return ast
        
    def exp(self):
        if self.accept('lit'):
            return Lit(self.token[1])
        else:
            return self.sub()
        
    def sub(self):
        self.expect('lparen')
        ast = self.alt()
        self.expect('rparen')
        return ast

def parse_one(source):
    p = RegexParser()
    return p.parse(source)

def parse_many(*source):
    p = RegexParser()
    for r in source:
        yield p.parse(r)


