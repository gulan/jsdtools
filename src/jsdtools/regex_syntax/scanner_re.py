#!python

"""
# re = lit | re (dot re)+ | re (bar re)+ | re star | '(' re ')'

 regex = lit | nest
  nest = '(' regex cont ')'
  cont = '*' | seq | alt
   seq = step +
  step = '.' regex
   alt = turn +
  turn = '|' regex
"""

import re

def Scanner(inp):

    PUNCT = set('.|*()')
    PD = {'.' : 'dot',
          '|' : 'bar',
          '*' : 'star',
          '(' : 'lparen',
          ')' : 'rparen'}
    
    def squeeze_blanks(s):
        return re.sub(r'[ ]+', ' ', s) # leave a space
    
    K = iter(squeeze_blanks(inp))

    def read():
        t = next(K, None)
        # print ('>> ', t)
        return t

    t = read()
    while t:
        if t == ' ':
            t = read()
        elif t in PUNCT:
            yield (PD[t], t)
            t = read()
        else:
            word = ''
            while t and t not in PUNCT and t != ' ':
                word += t
                t = read()
            yield ('lit', word)

def demo():
    def see(x):
        print (x, '->', list(Scanner(x)))

    see('abc')
    see('a b c')
    see(' a  b  c ')
    see('abc def ghi')
    see('abc . def* g|hi (w . v) ')



# def scan(inp):
#     return list(Scanner(inp))
