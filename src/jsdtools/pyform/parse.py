#!python

import re
import sys
# from jsdtools.ast import *
from .. ast import (Rep, Alt, Lit, Seq)

"""
For the scanner, a line begins with 0+ indents.
It continues with either one word and a newline, or
two words, a colon and a newline.

Dedent tokens are generated.
"""

class TokenError(Exception): pass

level = 0

def tokenize(line):
    global level
    (lead,more) = re.match(r'([ ]*)(.*)\n', line).groups()
    
    if len(lead) % 4 != 0:
        raise TokenError('bad indent: %r' % line)
    
    c = len(lead) // 4
    if c > level:
        level += 1
        yield ('indent', '')
    elif c < level:
        drop = level - c
        level = c
        for i in range(drop):
            yield ('dedent', '')
    
    words = [w for w in re.split(r'\s+', more) if w != '']

    if len(words) == 3:
        if words[0] in ('seq', 'alt', 'rep') and words[2] == ':':
            yield (words[0], '')
            yield ('lit', words[1])
            yield ('colon', ':')
        else:
            raise TokenError('bad line: %r' % line)
    elif len(words) == 2:
        if words[0] in ('seq', 'alt', 'rep') and words[1].endswith(':'):
            yield (words[0], '')
            yield ('lit', words[1][:-1])
            yield ('colon', ':')
        else:
            raise TokenError('bad line: %r' % line)
    elif len(words) == 1:
        yield ('lit', words[0])
    else:
        raise TokenError('too many tokens: %r' % line)

def scan(source=sys.stdin):
    global level
    for line in source:
        for tk in tokenize(line):
            yield tk
    while level > 0:
        yield ('dedent', '')
        level -= 1

class ParsingError(SyntaxError): pass

class Parser:

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
        return Lit(self.token[1])
    
    def seq(self):
        self.advance()
        name = self.token[1]
        self.expect('colon')
        self.expect('indent')
        m = []
        while not self.accept('dedent'):
            ast = self.tree()
            m.append(ast)
        ast = Seq(name)
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
        ast = Alt(name)
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
        ast = Rep(name)
        ast.add_child(s)
        return ast

def demo_scan():
    for i in scan():
        print (i)
    
def demo_parse():
    tokens = scan()
    p = PyformParser()
    ast = p.parse(tokens)
    print (ast)
