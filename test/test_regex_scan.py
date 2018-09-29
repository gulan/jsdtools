#!python

from jsdtools.regex.scan import Scanner

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

    assert list(Scanner('a:b')) == [
        ('lit', 'a'),
        ('colon', ':'),
        ('lit', 'b')]

    assert list(Scanner('(a):b5')) == [
        ('lparen', '('),
        ('lit', 'a'),
        ('rparen', ')'),
        ('colon', ':'),
        ('lit', 'b5')]

    assert list(Scanner('a . b:Q')) == [
        ('lit', 'a'),
        ('dot', '.'),
        ('lit', 'b'),
        ('colon', ':'),
        ('lit', 'Q')]

    assert list(Scanner('a . b : Q')) == [
        ('lit', 'a'),
        ('dot', '.'),
        ('lit', 'b'),
        ('colon', ':'),
        ('lit', 'Q')]

    assert list(Scanner('(a . b) : Q')) == [
        ('lparen', '('),
        ('lit', 'a'),
        ('dot', '.'),
        ('lit', 'b'),
        ('rparen', ')'),
        ('colon', ':'),
        ('lit', 'Q')]

    assert list(Scanner('((a*):W | b) : Q')) == [
        ('lparen', '('),
        ('lparen', '('),
        ('lit', 'a'),
        ('star', '*'),
        ('rparen', ')'),
        ('colon', ':'),
        ('lit', 'W'),
        ('bar', '|'),
        ('lit', 'b'),
        ('rparen', ')'),
        ('colon', ':'),
        ('lit', 'Q')]
