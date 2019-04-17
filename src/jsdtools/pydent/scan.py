#!python

# pyindent scan 
# TDB: get rid of global var

"""
The input is iterator yielding lines from a single pyindent form. Each
line is tokenised independently, except keeping track of the
indentation.

For the scanner, a line begins with 0+ indents.
It continues with either one word and a newline, or
two words, a colon and a newline.

An indent in the source is exactly four spaces.

Dedent tokens are generated as needed.
"""

import re
import sys

class TokenError(Exception): pass

KW = ('seq', 'alt', 'rep')
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
    # A deeply nested structure can drop several levels of indentation
    # with a single line.
    elif c < level:
        drop = level - c
        level = c
        for i in range(drop):
            yield ('dedent', '')
    
    words = [w for w in re.split(r'\s+', more) if w != '']

    # There might be a space before ':'
    if len(words) == 3:
        if words[0] in KW and words[2] == ':':
            yield (words[0], '')
            yield ('lit', words[1])
            yield ('colon', ':')
        else:
            raise TokenError('bad line: %r' % line)
    elif len(words) == 2:
        if words[0] in KW and words[1].endswith(':'):
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
    # source is an iterator of strings
    # the strings comprise one document
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
    
