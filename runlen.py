"""
Narative Specifcation
--------------------
An input string has runs of 1+ spaces between words (1+
non-space). The output is like the input except that every run of
spaces is replaced by a single space.

Formal
------
The input is an alternating sequence of words and gaps. Most simply,

    WGWGWGW

If so, 

    input = (W . G)* . W

If an empty input is possible:

    input = (W . G)* . [W]

or, equivalently:

    input = [W] . (G . W)*

But we might have gaps at the beginning, the end, or in both places.

    (1) <empty>
    (2) W
    (3) WGW
    (4) G
    (5) GWGW
    (6) WGWG
    (7) GWGWG

That is a lot of distinct cases. Two cases we cannot have are
subsequences of WW and GG, since an ajacent pair of words is really
just one larger word. The same goes for gaps. That is why I cannot
just say

    Xinput = (W | G)*

But this is correct:

    input = [W] . (G . W)* . [G]

    input' = maybe-word . repeats . maybe-gap
    repeats = gap-word*
    gap-word = gap . word

But a gap is an iteration of 1+ spaces, so [G] is [space+], which
reduces to space*.

    input'' = letter* . (space+ . letter+)* . space*

There is a recognition problem with space: we cannot tell which
instance it is until we have passed it. To help with this problem,
first make the end of the input an explict token.

    input''' = letter* . (S1 . letter+)* . S2 . eof
    S1 = space+
    S2 = space*

Now we can see that S1 is followed by a letter, and S2 is followed by
eof.

"""

EOF = '$'
SPACE = ' '

def runlen(ss):
    source = iter(ss)
    def aux():
        word = ''
        ch = source.next()
        while ch != EOF and ch != SPACE:
            word += ch
            ch = source.next()
        if word:
            yield word
        while ch != EOF:
            cnt = 0
            while ch != EOF and ch == SPACE:
                cnt += 1
                ch = source.next()
            if cnt > 0:
                yield SPACE
            word = ''
            while ch != EOF and ch != SPACE:
                word += ch
                ch = source.next()
            if word:
                yield word
        cnt = 0
        while ch != EOF and ch == SPACE:
            cnt += 1
            ch = source.next()
        if cnt > 0:
            yield SPACE
        assert ch == '$'
        yield ch
    return ''.join(list(aux()))

def test():
    assert runlen('$') == '$'
    assert runlen('abc$') == 'abc$'
    assert runlen('abc   def$') == 'abc def$'
    assert runlen('   $') == ' $'
    assert runlen('   abc   def$') == ' abc def$'
    assert runlen('abc   def   $') == 'abc def $'
    assert runlen('  abc   def   $') == ' abc def $'
    print 'ok'

if __name__ == '__main__':
    test()
