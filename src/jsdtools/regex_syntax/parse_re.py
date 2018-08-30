#!python

"""
       G = '(' X ')'
       X = REP | SEQ | ALT | LIT
     REP = 'rep'  LABEL G
    REP1 = 'rep+' LABEL G
     SEQ = 'seq'  LABEL '[' G+ ']'
     ALT = 'alt'  LABEL '[' G+ ']'
     LIT = 'lit'  LITERAL

"""

from jsdtools.abstract_jsp_ast import Rep, Rep1, Alt, Lit, Seq
# from jsdtools.regex_syntax.scanner_re import Scanner
from scanner_re import Scanner

"""
# re = lit | re (dot re)+ | re (bar re)+ | re star | '(' re ')'

 regex = lit | nest
  nest = '(' regex cont ')'
  cont = '*' | seq | alt
   seq = step step*
  step = '.' regex
   alt = turn turn*
  turn = '|' regex

"""

class ParsingError(SyntaxError): pass

class Parser:

    def parse(self, source):
        print('------------  %s  ------------' % source)
        self.G = Scanner(source)
        self.token = self.next_token = None
        self.advance()
        self.start()

    def advance(self):
        self.token, self.next_token = self.next_token, next(self.G, None)

    def accept(self, toktype):
        if self.next_token and self.next_token[0] == toktype:
            print('accept>', self.next_token)
            self.advance()
            return True
        else:
            return False

    def expect(self, t):
        if not self.accept(t):
            raise ParsingError('Expected ' + t)
        
class ReParser(Parser):
    
    """
      regex = lit | '(' regex cont ')'
       cont = '*' | '.' regex ('.' regex)* | '|' regex ('|' regex)*
    """

    def start(self):
        return self.regex()
    
    def regex(self):
        if self.accept('lit'):
            pass
        else:
            self.expect('lparen')
            self.regex()
            self.cont()
            self.expect('rparen')
        
    def cont(self):
        if self.accept('star'):
            pass
        elif self.accept('dot'):
            self.regex()
            while self.accept('dot'):
                self.regex()
        else:
            self.expect('bar')
            self.regex()
            while self.accept('bar'):
                self.regex()

class RegexParser(Parser):
    """    
    alt = seq ('|' seq)*
    seq = rep ('.' rep)*
    rep = xxx ('*')*
    xxx = lit  |  '(' alt ')'
    """

    def start(self): self.alt()
    
    def alt(self):
        self.seq()
        while self.accept('bar'):
            self.seq()
    
    def seq(self):
        self.rep()
        while self.accept('dot'):
            self.rep()
            
    def rep(self):
        self.xxx()
        while self.accept('star'):
            pass
    
    def xxx(self):
        if self.accept('lit'):
            pass
        else:
            self.expect('lparen')
            self.alt()
            self.expect('rparen')

def split_cases(p,tc):
    for i in tc.split('\n'):
        if not i: continue
        if i.startswith('-'):
            pass
        else:
            p.parse(i)
    
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
"""

split_cases(RegexParser(), tc)

print('ok')



tc_for_reparser = """
a
A
-|
(a*)
(a|b)
(a|b|c)
(a|(b*))
(a . (b*) . (c | d))
"""

"""
alt = alt '|' seq  |  seq
seq = seq '.' rep  |  rep
rep = rep '*'  |  xxx
xxx = lit  |  '(' alt ')'

alt                                       :  x
seq ('|' seq)*                            :  x
(rep ('.' rep)*) ('|' seq)*               :  x
((xxx ('*')*) ('.' rep)*) ('|' seq)*      :  x
((lit ('*')*) ('.' rep)*) ('|' seq)*      :  x
(('*')* ('.' rep)*) ('|' seq)*            :  
('.' rep)* ('|' seq)*                     :  
('|' seq)*                                :  
                                          :  

alt     :  x
seq ... :  x
rep ... :  x
xxx ... :  x
lit ... :  x
        :  

"""
