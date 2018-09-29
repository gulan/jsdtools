#!python

import io
from jsdtools.regex.render import (printer, walk, print_ast)
from jsdtools.regex.parse import (ParsingError, RegexParser, parse_one)

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
