#!python

# TDB: get rid of global var

"""
For the scanner, a line begins with 0+ indents.
It continues with either one word and a newline, or
two words, a colon and a newline.

An indent is exactly four spaces.

Dedent tokens are generated as needed.
"""

import re
import sys

class TokenError(Exception): pass

level = 0

def tokenize(line):
    global level
    (lead,more) = re.match(r'([ ]*)(.*)\n', line).groups()
    
    if len(lead) % 4 != 0:
        raise TokenError('bad indent: %r' % line)
    
    c = len(lead) // 4
    if c > level:
        level += 1
        yield ('indent', '')
    elif c < level:
        drop = level - c
        level = c
        for i in range(drop):
            yield ('dedent', '')
    
    words = [w for w in re.split(r'\s+', more) if w != '']

    if len(words) == 3:
        if words[0] in ('seq', 'alt', 'rep') and words[2] == ':':
            yield (words[0], '')
            yield ('lit', words[1])
            yield ('colon', ':')
        else:
            raise TokenError('bad line: %r' % line)
    elif len(words) == 2:
        if words[0] in ('seq', 'alt', 'rep') and words[1].endswith(':'):
            yield (words[0], '')
            yield ('lit', words[1][:-1])
            yield ('colon', ':')
        else:
            raise TokenError('bad line: %r' % line)
    elif len(words) == 1:
        yield ('lit', words[0])
    else:
        raise TokenError('too many tokens: %r' % line)

def scan_one(source=sys.stdin):
    global level
    for line in source:
        for tk in tokenize(line):
            yield tk
    while level > 0:
        yield ('dedent', '')
        level -= 1

def demo_scan():
    for i in scan_one():
        print (i)
    
