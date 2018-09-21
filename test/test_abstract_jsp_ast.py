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

def test_eq():
    s = Lit('s')
    t = Lit('s')
    u = Lit('u')
    assert s == t
    assert id(s) != id(t)
    assert s != u
    
    ss0 = Seq('ss')
    [ss0.add_child(Lit(n)) for n in "abcdef"]
    ss1 = Seq('ss')
    [ss1.add_child(Lit(n)) for n in "abcdef"]
    assert ss0 == ss1

    aa0 = Alt('aa')
    aa0.add_child(ss0)
    aa0.add_child(s)
    aa1 = Alt('aa')
    aa1.add_child(ss1)
    aa1.add_child(t)
    assert aa0 == aa1

    rr0 = Rep('rr')
    rr0.add_child(aa0)
    rr1 = Rep('rr')
    rr1.add_child(aa1)
    assert rr0 == rr1
    
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
