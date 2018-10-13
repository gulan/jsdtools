#!python

import re
import string

TAG = {'.' : 'dot',
       '|' : 'bar',
       '*' : 'star',
       ':' : 'colon',
       '(' : 'lparen',
       ')' : 'rparen'}

PUNCT = frozenset(TAG.keys())
CHARS = frozenset(string.ascii_letters + "-_'" + string.digits)
VALID = PUNCT | CHARS 
   
class ScanError(Exception): pass

def Scanner(inp):

    def squeeze_blanks(s):
        return re.sub(r'\s+', ' ', s) # leave a space
    
    K = iter(squeeze_blanks(inp))

    def read():
        t = next(K, None)
        return t

    t = read()
    while t:
        if t == ' ':
            t = read()
            continue
        
        if t not in VALID:
            raise ScanError(t)
        
        if t in PUNCT:
            yield (TAG[t], t)
            t = read()
            continue
        
        word = ''
        while t and t in CHARS:
            word += t
            t = read()
        yield ('lit', word)

def demo():
    
    def see(x):
        print (repr(x), '->', list(Scanner(x)))

    see('abc')
    see('a b c')
    see(' a  b  c ')
    see('abc def ghi')
    see('a1 . d1* g|h1 (w . v) ')
    see('.|*()')
    see("A BC 2 34 D_E G-F a'")
    see('a . B:(x | y) . c')
    print ('---------------')
    see('a:b')
    see('(a):b5')
    see('a . b:Q')
    see('a . b : Q')
    see('(a . b) : Q')
    see('((a*):W | b) : Q')

def scan_one(source):
    return Scanner(source)
