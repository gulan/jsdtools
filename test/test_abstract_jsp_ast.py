#!python

from jsdtools.abstract_jsp_ast import (Lit, Seq, Alt, Rep)

def test_repr_lit():
    assert repr(Lit('alpha')) == '(lit alpha)'
    
def test_repr_seq():
    s = Seq('seq1')
    s.add_child(Lit('alpha'))
    s.add_child(Lit('beta'))
    s.add_child(Lit('gamma'))
    assert repr(s) == '(seq seq1 [(lit alpha) (lit beta) (lit gamma)])'
    
def test_repr_alt():
    s = Alt('alt1')
    s.add_child(Lit('alpha'))
    s.add_child(Lit('beta'))
    s.add_child(Lit('gamma'))
    assert repr(s) == '(alt alt1 [(lit alpha) (lit beta) (lit gamma)])'
    
def test_repr_rep():
    s = Rep('repX')
    s.add_child(Lit('alpha'))
    assert repr(s) == '(rep repX (lit alpha))'
    
# if __name__ == '__main__':
#     p = Lit('alpha')
    
#     q = Seq('seq1')
#     q.add_child(Lit('alpha'))
#     q.add_child(Lit('beta'))
#     q.add_child(Lit('gamma'))
    
#     r = Alt('alt1')
#     r.add_child(Lit('alpha'))
#     r.add_child(Lit('beta'))
#     r.add_child(Lit('gamma'))
    
#     s = Rep('repX')
#     s.add_child(Lit('alpha'))
    
#     print (p.labels())
#     print (q.labels())
#     print (r.labels())
#     print (s.labels())
#     print ('-' * 40)
#     print (p.anno())
#     print (q.anno())
#     print (r.anno())
#     print (s.anno())
#     print ('-' * 40)
#     print (p.graph())
#     print (q.graph())
#     print (r.graph())
#     print (s.graph())

