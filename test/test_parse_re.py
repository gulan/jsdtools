#!python

from jsdtools.abstract_jsp_ast import (Lit, Seq, Alt, Rep)
from jsdtools.regex_syntax.parse_re import (ParsingError, RegexParser)

def test_parse_lit():
    p =  RegexParser()
    assert repr(p.parse('a')) == repr(Lit('a'))
    assert repr(p.parse('abc')) == repr(Lit('abc'))
    assert repr(p.parse('a_b-c\'')) == repr(Lit('a_b-c\''))
    assert repr(p.parse('123')) == repr(Lit('123'))
    assert repr(p.parse('_')) == repr(Lit('_'))
    
def test_parse_rep():
    p = RegexParser()
    def parse(x):
        return p.parse(x, True)
    def mkrep(x):
        r = Rep('_0')
        r.add_child(x)
        return r
    assert repr(parse('a*')) == repr(mkrep(Lit('a')))
    assert repr(parse('abc*')) == repr(mkrep(Lit('abc')))
    assert repr(parse('a**')) == repr(mkrep(Lit('a'))) # my hackish optimization
    
def test_parse_seq():
    p = RegexParser()
    def parse(x):
        return p.parse(x, True)
    def mkseq(xs):
        r = Seq('_0')
        for x in xs:
            r.add_child(x)
        return r
    assert repr(parse('a . b')) == repr(mkseq([Lit('a'),Lit('b')]))
    assert repr(parse('a . b . c ')) == repr(mkseq([Lit('a'),Lit('b'),Lit('c')]))
    
def test_parse_alt():
    p = RegexParser()
    def parse(x):
        return p.parse(x, True)
    def mkalt(xs):
        r = Alt('_0')
        for x in xs:
            r.add_child(x)
        return r
    assert repr(parse('a | b')) == repr(mkalt([Lit('a'),Lit('b')]))
    assert repr(parse('a | b | c ')) == repr(mkalt([Lit('a'),Lit('b'),Lit('c')]))

def test_parse_precedence():
    """ AST nodes of lower precedence are higher in the ast tree. """
    p = RegexParser()
    assert type(p.parse('(a . b | c)')).__name__ == 'Alt'
    assert type(p.parse('(a | b . c)')).__name__ == 'Alt'
    assert type(p.parse('(a* | b* . c*)')).__name__ == 'Alt'
    assert type(p.parse('(a* . b* | c*)')).__name__ == 'Alt'
    assert type(p.parse('(a* . b* . c*)')).__name__ == 'Seq'
    

def test_parse_grouping(): pass

# def display_tree(r):
#     p = RegexParser()
#     ast = p.parse(r)
#     for (level, _, node, name, _) in ast.walk():
#         print('    ' * level, node, name)

# if 1:
#     p = RegexParser()
#     print (p.parse('a . (b . c)'))
#     print (p.parse('(a . b) . c'))
    
#     print (p.parse('a | (b | c)'))
#     print (p.parse('(a | b) | c'))

#     print (p.parse('a . (b | c)'))
#     print (p.parse('(a | b) . c'))

#     print (p.parse('a | (b . c)'))
#     print (p.parse('(a . b) | c'))

#     print ('---------')
#     display_tree('(a | b . c)')
#     display_tree('(a . b | c)')
    
#     # print (Lit('a'))
    
"""    

'a'
(lit a)
'a*'
(rep _0 (lit a))
'a**'
(rep _0 (lit a))
'(a)'
(lit a)
'a | b'
(alt _0 [(lit a) (lit b)])
'a | b | c'
(alt _0 [(lit a) (lit b) (lit c)])
'a.b.c'
(seq _0 [(lit a) (lit b) (lit c)])
'a*|b'
(alt _0 [(rep _0 (lit a)) (lit b)])
'a|b*'
(alt _0 [(lit a) (rep _0 (lit b))])
'a*.b'
(seq _0 [(rep _0 (lit a)) (lit b)])
'(a* . b* .c*)'
(seq _0 [(rep _0 (lit a)) (rep _0 (lit b)) (rep _0 (lit c))])
'(a* . b* .c*)*'
(rep _0 (seq _0 [(rep _0 (lit a)) (rep _0 (lit b)) (rep _0 (lit c))]))
'(a . b | c)'
(alt _0 [(seq _0 [(lit a) (lit b)]) (lit c)])
'(a | b . c)'
(alt _0 [(lit a) (seq _0 [(lit b) (lit c)])])
'((a))*'
(rep _0 (lit a))
'((a)*)*'
(rep _0 (rep _0 (lit a)))
'((a*)*)*'
(rep _0 (rep _0 (rep _0 (lit a))))
'((a.b)*)*'
(rep _0 (rep _0 (seq _0 [(lit a) (lit b)])))
"""
