#!python

import jsdtools.lisp as lisp

def test_parse_many():
    a = '(lit alpha)'
    b = '(rep name (lit alpha))'
    c = '(seq name [(lit alpha) (lit beta) (lit gamma)])'
    d = '(alt name [(lit alpha) (lit beta) (lit gamma)])'
    expect = [a,b,c,d]
    actual = list(lisp.parse_many(''.join(expect)))
    assert list(map(repr, actual)) == expect
