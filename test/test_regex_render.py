#!python

import io
from jsdtools.regex.render import (printer, walk)
from jsdtools.regex import (parse_one, print_one)

def my_print_ast(ast):
    # render to string with no newline
    sf = io.StringIO()
    p = printer(out=sf)
    walk(p, ast)
    r = sf.getvalue()
    sf.close()
    return r
    
def test_inverse():
    def identity(r):
        return my_print_ast(parse_one(r)) == r
    assert identity('a')
    assert identity('(a . b)')
    assert identity('(a . b . c)')
    assert identity('((a . b) . c)')
    assert identity('(a . (b . c))')
    
    assert identity('(a | b)')
    assert identity('(a | b | c)')
    assert identity('((a | b) | c)')
    assert identity('(a | (b | c))')

    assert identity('a*')
    assert identity('a**')
