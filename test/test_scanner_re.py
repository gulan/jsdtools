#!python

from jsdtools.regex_syntax.scanner_re import Scanner

def test_scan():
    
    assert list(Scanner('abc')) == [('lit', 'abc')]

    assert list(Scanner('a b c')) == [
        ('lit', 'a'),
        ('lit', 'b'),
        ('lit', 'c')]

    assert list(Scanner(' a  b  c ')) == [
        ('lit', 'a'),
        ('lit', 'b'),
        ('lit', 'c')]

    assert list(Scanner('abc def ghi')) == [
        ('lit', 'abc'),
        ('lit', 'def'),
        ('lit', 'ghi')]

    assert list(Scanner('a1 . d1* g|h1 (w . v) ')) == [
        ('lit', 'a1'),
        ('dot', '.'),
        ('lit', 'd1'),
        ('star', '*'),
        ('lit', 'g'),
        ('bar', '|'),
        ('lit', 'h1'),
        ('lparen', '('),
        ('lit', 'w'),
        ('dot', '.'),
        ('lit', 'v'),
        ('rparen', ')')]

    assert list(Scanner('.|*()')) == [
        ('dot', '.'),
        ('bar', '|'),
        ('star', '*'),
        ('lparen', '('),
        ('rparen', ')')]

    assert list(Scanner("A BC 2 34 D_E G-F a'")) == [
        ('lit', 'A'),
        ('lit', 'BC'),
        ('lit', '2'),
        ('lit', '34'),
        ('lit', 'D_E'),
        ('lit', 'G-F'),
        ('lit', "a'")]
