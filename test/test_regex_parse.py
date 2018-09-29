#!python

from jsdtools.ast import (Lit, Seq, Alt, Rep)
from jsdtools.regex.parse import (ParsingError, RegexParser)

def test_parse_lit_repr():
    p =  RegexParser()
    assert repr(p.parse('a')) == repr(Lit('a'))
    assert repr(p.parse('abc')) == repr(Lit('abc'))
    assert repr(p.parse('a_b-c\'')) == repr(Lit('a_b-c\''))
    assert repr(p.parse('123')) == repr(Lit('123'))
    assert repr(p.parse('_')) == repr(Lit('_'))
    
def test_parse_lit_eq():
    p =  RegexParser()
    assert p.parse('a') == Lit('a')
    assert p.parse('abc') == Lit('abc')
    assert p.parse('a_b-c\'') == Lit('a_b-c\'')
    assert p.parse('123') == Lit('123')
    assert p.parse('_') == Lit('_')
    
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
    # assert repr(parse('a**')) == repr(mkrep(Lit('a'))) # my hackish optimization
    assert parse('a*') == mkrep(Lit('a'))
    assert parse('abc*') == mkrep(Lit('abc'))
    # assert parse('a**') == mkrep(Lit('a')) # my hackish optimization
    
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
    assert parse('a . b') == mkseq([Lit('a'),Lit('b')])
    assert parse('a . b . c ') == mkseq([Lit('a'),Lit('b'),Lit('c')])
    
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
    assert parse('a | b') == mkalt([Lit('a'),Lit('b')])
    assert parse('a | b | c ') == mkalt([Lit('a'),Lit('b'),Lit('c')])

def test_parse_precedence():
    """ AST nodes of lower precedence are higher in the ast tree. """
    p = RegexParser()
    assert type(p.parse('(a . b | c)')).__name__ == 'Alt'
    assert type(p.parse('(a | b . c)')).__name__ == 'Alt'
    assert type(p.parse('(a* | b* . c*)')).__name__ == 'Alt'
    assert type(p.parse('(a* . b* | c*)')).__name__ == 'Alt'
    assert type(p.parse('(a* . b* . c*)')).__name__ == 'Seq'
    

def test_parse_grouping_seq():
    # TBD: make blackbox
    p = RegexParser()
    right = p.parse('a . (b . c)')
    assert right.ntype == 'seq'
    assert len(right.child) == 2
    assert right.child[0].ntype == 'lit'
    assert right.child[1].ntype == 'seq'
    
    left = p.parse('(a . b) . c')
    assert left.ntype == 'seq'
    assert len(left.child) == 2
    assert left.child[0].ntype == 'seq'
    assert left.child[1].ntype == 'lit'

def test_parse_grouping_alt():
    p = RegexParser()
    right = p.parse('a | (b | c)')
    assert right.ntype == 'alt'
    assert len(right.child) == 2
    assert right.child[0].ntype == 'lit'
    assert right.child[1].ntype == 'alt'
    
    left = p.parse('(a | b) | c')
    assert left.ntype == 'alt'
    assert len(left.child) == 2
    assert left.child[0].ntype == 'alt'
    assert left.child[1].ntype == 'lit'

def test_parse_grouping_mixed():
    p = RegexParser()
    
    g = p.parse('a . (b | c)')
    assert g.ntype == 'seq'
    assert len(g.child) == 2
    assert g.child[0].ntype == 'lit'
    assert g.child[1].ntype == 'alt'
    
    g = p.parse('(a | b) . c')
    assert g.ntype == 'seq'
    assert len(g.child) == 2
    assert g.child[0].ntype == 'alt'
    assert g.child[1].ntype == 'lit'

    g = p.parse('a | (b . c)')
    assert g.ntype == 'alt'
    assert len(g.child) == 2
    assert g.child[0].ntype == 'lit'
    assert g.child[1].ntype == 'seq'
    
    g = p.parse('(a . b) | c')
    assert g.ntype == 'alt'
    assert len(g.child) == 2
    assert g.child[0].ntype == 'seq'
    assert g.child[1].ntype == 'lit'
    
def test_parse_grouping_nested():
    p = RegexParser()
    assert p.parse('(a)') == p.parse('a')
    assert p.parse('((a))') == p.parse('a')
    assert p.parse('(a.b)') == p.parse('a.b')
    assert p.parse('(a.(b))') == p.parse('a.b')
    assert p.parse('(a|b)') == p.parse('a|b')
    assert p.parse('(a|(b))') == p.parse('a|b')
    assert p.parse('((a)*)') == p.parse('a*')

def test_parse_labels():
    p = RegexParser()
    assert p.parse('a').label == 'a'
    assert p.parse('a:A').label == 'A'
    assert p.parse('(a):A').label == 'A'
    assert p.parse('((a)):A').label == 'A'
    assert p.parse('(a*):A').label == 'A'
    assert p.parse('(a.b):A').label == 'A'
    assert p.parse('(a|b):A').label == 'A'
    assert p.parse('((a:X)*):A').label == 'A'
    assert p.parse('((a:X).b):A').label == 'A'
    assert p.parse('(a|(b:X)):A').label == 'A'
    assert p.parse('(a:A):B').label == 'B'
