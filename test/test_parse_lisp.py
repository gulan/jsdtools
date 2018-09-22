#!python

from jsdtools.lisp.parse import (scan, parse_one, parse_many)

def test_scanner_lit():
    a = scan('(lit alpha)')
    b = scan(' (  lit   alpha ) ')
    c = scan('\n(\nlit \nalpha\n)\n')
    expect = ['(', 'lit', 'alpha', ')', '$']
    assert a == expect
    assert a == b
    assert b == c
    
def test_scanner_seq():
    expect = ['(', 'seq', '[', '(', 'lit', 'alpha', ')',
              '(', 'lit', 'beta', ')',
              '(', 'lit', 'gamma', ')', ']', ')', '$']
    assert scan('(seq [(lit alpha) (lit beta) (lit gamma)])') == expect
    assert scan(' '.join(expect[:-1])) == expect
    assert scan('\n'.join(expect[:-1])) == expect

def test_scanner_alt():
    expect = ['(', 'alt', '[', '(', 'lit', 'alpha', ')',
              '(', 'lit', 'beta', ')',
              '(', 'lit', 'gamma', ')', ']', ')', '$']
    assert scan('(alt [(lit alpha) (lit beta) (lit gamma)])') == expect
    assert scan(' '.join(expect[:-1])) == expect
    assert scan('\n'.join(expect[:-1])) == expect

def test_scanner_rep():
    expect = ['(', 'rep', '(', 'lit', 'alpha', ')', ')', '$']
    assert scan('(rep (lit alpha))') == expect
    assert scan(' '.join(expect[:-1])) == expect
    assert scan('\n'.join(expect[:-1])) == expect

def test_comment():
    pass # TBD

def test_parse_one():
    a = '(lit alpha)'
    b = '(rep name (lit alpha))'
    c = '(seq name [(lit alpha) (lit beta) (lit gamma)])'
    d = '(alt name [(lit alpha) (lit beta) (lit gamma)])'
    assert repr(parse_one(a)) == a
    assert repr(parse_one(b)) == b
    assert repr(parse_one(c)) == c
    assert repr(parse_one(d)) == d
    
def test_parse_many():
    a = '(lit alpha)'
    b = '(rep name (lit alpha))'
    c = '(seq name [(lit alpha) (lit beta) (lit gamma)])'
    d = '(alt name [(lit alpha) (lit beta) (lit gamma)])'
    expect = [a,b,c,d]
    actual = list(parse_many(''.join(expect)))
    assert list(map(repr, actual)) == expect
