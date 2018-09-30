#!python

import re

def Scanner(inp):
    # Convert `inp` string to sequence of tokens
    PUNCT = list(iter('()[]'))
    
    def filter_comments(text):
        return ''.join(m for m in text
                       if not m.startswith('#') and not m.startswith(';'))

    def squeeze_blanks(s):
        s = s.replace('\t',' ')
        s = s.replace('\n',' ')
        return re.sub(r'[ ]+', ' ', s) # leave a space
    
    K = iter(squeeze_blanks(filter_comments(inp) + '$'))
    
    t = next(K)
    while t != '$': # the $ is my made-up end-of-string token.
        if t == ' ':
            t = next(K)
        elif t in PUNCT:
            yield t
            t = next(K)
        else: # keywords and literals are undistinguished
            word = ''
            while t != '$' and t not in PUNCT and t != ' ':
                word += t
                t = next(K)
            yield word
    yield '$'

def scan_one(inp):
    # The input can have several complete lisp expressions concatented
    # together. That works fine.
    return Scanner(inp)
