#!python

# regex scanner

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

def Scanner(source):

    def squeeze_blanks(s):
        return re.sub(r'\s+', ' ', s) # leave a space

    # s = ''.join(source)
    K = iter(squeeze_blanks(source))

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

def scan_one(text):
    assert isinstance(text, str)
    return Scanner(text)
