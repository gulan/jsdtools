#!python

from itertools import count, cycle
from jsdtools.abstract_jsp_ast import Rep, Rep1, Alt, Lit, Seq
from jsdtools.regex_syntax.scanner_re import Scanner
# from scanner_re import Scanner

class ParsingError(SyntaxError): pass

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

class RegexParser(Parser):
    """    
    alt = seq ('|' seq)*
    seq = rep ('.' rep)*
    rep = xxx ('*')*
    xxx = lit  |  '(' alt ')'
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
        ast = self.xxx()
        c = 0
        while self.accept('star'):
            c += 1
        if c > 0:
            n = Rep(self.name())
            n.add_child(ast)
            return n
        else:
            return ast
    
    def xxx(self):
        if self.accept('lit'):
            return Lit(self.token[1])
        else:
            self.expect('lparen')
            ast = self.alt()
            self.expect('rparen')
            return ast

tc = """
a
a*
a**
(a)
a | b
a | b | c
a.b.c
a*|b
a|b*
a*.b
(a* . b* .c*)
(a* . b* .c*)*
(a . b | c)
(a | b . c)
((a))*
((a)*)*
((a*)*)*
((a.b)*)*
"""

if __name__ == '__main__':
    
    def split_cases(p,tc):
        for i in tc.split('\n'):
            if not i: continue
            if i.startswith('-'):
                pass
            else:
                print (repr(i))
                ast = p.parse(i, test_counter=True)
                print (ast)
    

    split_cases(RegexParser(), tc)
