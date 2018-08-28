#! /usr/bin/env python

"""
phase one: parse regex to its ast

I realized that a JSP tree is really much like the ast of a regular
expression. The differences are:

* the internal nodes of a JSP tree are given meaningfull names by the
  author. The internal nodes of a regex are anonymous.

When producing the jsp tree, I must synthesize names for the internal
nodes.

a . b -> (seq _1 [(lit a) (lit b)]) 
a | b -> (alt _1 [(lit a) (lit b)])
a*    -> (rep _1 (lit a))

(a . b)* -> (rep _1 (seq _2 [(lit a) (lit b)]))

Remember that '*' means different things for the re and jsp. In re, it
denotes a replication and it child expression is the what is
replicated. In JSP it is the child of a node that carries the *. This
later convention adds a trap for the beginging diagrammer: they must
be sure not to mark child nodes inconsistently. With a regex, it is
impossible to express this limitation.

But the regex does have a limitation of it own: the sequence operator
is infix, so there is no way to express as sequence of one item. It
is useful to be able to do this.

I cannot expression a singleton alternation either, but (a | a) is a
substitue.

I could also have zero-ary sequences and alternations, but I do not
see the need for them.

re = lit | seq | alt | rep | sub
lit = word
seq = re . dot . (re . dot)* . re
alt = re . bar . (re . bar)* . re
rep = re . star
sub = '(' . re . ')'

re = lit | com | sub
com = re . (seq | alt | rep)
lit = word
seq = dot . (re . dot)* . re
alt = bar . (re . bar)* . re
rep = star
sub = '(' . re . ')'

re = lit | com
lit = word
com = re . (seq | alt | rep)
seq = dot . (re . dot)* . re
alt = bar . (re . bar)* . re
rep = star

re = lit . (seq | rep | -)
seq = dot . (lit . dot)* . lit
rep = star
"""

import sys
from spark7 import (GenericScanner, GenericParser)
from jsdtools.abstract_jsp_ast import (Lit, Seq, Alt, Rep)

"""
re = lit . (seq | rep | -)
seq = dot . (lit . dot)* . lit
rep = star
"""

def mkgensym():
    def gensym():
        i = 0
        while 1:
            yield "_%s" % i
            i += 1
    return gensym()

class Token:

    def __init__(self, type, attr=None):
        self.type = type
        self.attr = attr

    def __repr__(self):
        if self.attr:
            return "T(%s,%s)" % (self.type, self.attr)
        else:
            return "T(%s)" % self.type

    def __cmp__(self, other):
        return cmp(self.type, other)

class Scanner(GenericScanner):

    def __init__(self):
        GenericScanner.__init__(self)

    def tokenize(self, inp):
        self.rv = []
        GenericScanner.tokenize(self,inp)
        return self.rv

    def t_whitespace(self, s):
        r'\s+'
        pass

    def t_star(self, s):
        r' \* '
        self.rv.append(Token(type='*'))

    def t_bar(self, s):
        r' \| '
        self.rv.append(Token(type='|'))

    def t_dot(self, s):
        r' \. '
        self.rv.append(Token(type='.'))

    def t_open(self, s):
        r' \( '
        self.rv.append(Token(type='('))

    def t_close(self, s):
        r' \) '
        self.rv.append(Token(type=')'))
        
    def t_literal(self, s):
        r'[a-z0-9_\-]+'
        self.rv.append(Token(type='LIT', attr=s))

class ExprParser(GenericParser):

    def __init__(self, start='re'):
        GenericParser.__init__(self, start)
        self._gensym = mkgensym()

    def p_re_1(self, args):
        ' re ::= seq '
        # print 're_1>> ', args[0]
        return args[0]

    def p_re_2(self, args):
        ' re ::= rep '
        # print 're_2>> ', args[0]
        return args[0]

    def p_re_3(self, args):
        ' re ::= alt '
        # print 're_3>> ', args[0]
        return args[0]

    def p_seq_1(self, args):
        ' seq ::= seq . exp '
        args[0].add_child(args[2])
        # print 'seq_1>> ', args[0]
        return args[0]

    def p_seq_2(self, args):
        ' seq ::= exp '
        w = Seq(self._gensym.next())
        w.add_child(args[0])
        # print 'seq_2>> ', w
        return w

    def p_alt_1(self, args):
        ' alt ::= alt | exp '
        args[0].add_child(args[2])
        # print 'alt_1>> ', args[0]
        return args[0]

    def p_alt_2(self, args):
        ' alt ::= exp '
        w = Alt(self._gensym.next())
        w.add_child(args[0])
        # print 'alt_2>> ', w
        return w

    # a* ==> (rep _1 (lit a))
    def p_rep(self, args):
        ' rep ::= exp * '
        # print 'rep>> ', args
        w = Rep(self._gensym.next())
        w.add_child(args[0])
        return w

    def p_exp_1(self, args):
        ' exp ::= LIT '
        w = Lit(args[0].attr)
        # print 'exp_1>> ', w
        return w

    def p_exp_2(self, args):
        ' exp ::= ( re ) '
        # print 'exp_2>> ', args[1]
        return args[1]

def re_to_ast(regex):
    s = Scanner()
    r = s.tokenize(regex)
    p = ExprParser()
    ast = p.parse(r)
    return ast

def test_parse():
    assert repr(re_to_ast('a')) == '(seq _0 [(lit a)])'
    assert repr(re_to_ast('a.b')) == '(seq _0 [(lit a) (lit b)])'
    assert repr(re_to_ast('a|b')) == '(alt _0 [(lit a) (lit b)])'
    assert repr(re_to_ast('a*')) == '(rep _0 (lit a))'
    assert repr(re_to_ast('a.b.c')) == '(seq _0 [(lit a) (lit b) (lit c)])'
    assert repr(re_to_ast('(a.b).c')) == '(seq _1 [(seq _0 [(lit a) (lit b)]) (lit c)])'
    assert repr(re_to_ast('a.(b.c)')) == '(seq _1 [(lit a) (seq _0 [(lit b) (lit c)])])'
    assert repr(re_to_ast('a|b|c')) == '(alt _0 [(lit a) (lit b) (lit c)])'
    assert repr(re_to_ast('(a|b)|c')) == '(alt _1 [(alt _0 [(lit a) (lit b)]) (lit c)])'
    assert repr(re_to_ast('a|(b|c)')) == '(alt _1 [(lit a) (alt _0 [(lit b) (lit c)])])'
    assert repr(re_to_ast('(a|b)*')) == '(rep _1 (alt _0 [(lit a) (lit b)]))'
    assert repr(re_to_ast('(a*)|b')) == '(alt _1 [(rep _0 (lit a)) (lit b)])'
    assert repr(re_to_ast('((a*)|b)*')) == '(rep _2 (alt _1 [(rep _0 (lit a)) (lit b)]))'
    assert repr(re_to_ast('(cat|dog)*')) == '(rep _1 (alt _0 [(lit cat) (lit dog)]))'


# def s1():
#     ast = re_to_ast('(meet . (award*))*')
#     dict = {'_0':'work','_1':'period','_2':'panel'}
#     ast.relabel(dict)
#     ast2dot.render_one(ast)

# def s2():
#     ast = re_to_ast('sunscribe . (enter*)')
#     ast.relabel({'_0':'reader-body','_1':'reader'})
#     ast2dot.render_one(ast)

# if 0:
#     ast = re_to_ast('buy . ((use|bind)*)')
#     ast.relabel({'_0':'event','_1':'book-body', '_2':'book'})
#     ast2dot.render_one(ast)

# if 0:
#     ast = re_to_ast("bind . (bindx*)")
#     # ast.relabel({'_0':'event','_1':'book-body', '_2':'book'})
#     ast2dot.render_one(ast)

if __name__ == '__main__':
    regex = sys.argv[1]
    d = {}
    for (pos,name) in enumerate(sys.argv[2:]):
        k = "_%d" % pos
        d[k] = name
    ast = re_to_ast(regex)
    ast.relabel(d)
    print ast
