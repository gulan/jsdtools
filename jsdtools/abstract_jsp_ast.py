#!/usr/bin/python

# TBD: children() or children_of() ?

"""
type Label = String
data JSP =   Lit Label
           | Seq Label [JSP]
           | Alt Label [JSP]
           | Rep Label JSP

Each node has a uid.
  * retains identity even if labels change
  * lists of tuples of nodeid permit graph processing
  * what about t.copy()?
  * what about serialization?
  * why not use object id?

Each node has a string field naming its class.
  * Why? Python nodes already know their class

Most computation on JSP starts by converting the tree to a graph.
  * Why have two representations?
  * Why does the graph no have Lit nodes?

Abstract and Compound classes seem more about avoiding code
duplication than hiding the implementation.

"""

def mkseqno():
    n = 10
    while 1:
        yield n
        n += 1

seqno = mkseqno()

class Abstract(object):
    
    """
    The Concrete AST uses the composite pattern. This Abstract class
    is the common API.
    
    # TBD: move out the __init__ as it is particular to the implementation.
    """
    
    def __init__(self, label):
        self.child = []
        self.label = label    # string type
        self.ntype = self.__class__.__name__.lower()
        self.sn = seqno.next()

    def __repr__(self): raise NotImplemented
    
    def anno(self):
        """The compound nodes (alt and rep) are shown on the output
        tree by marks (* or o) on their child nodes. The anno method
        builds a map from each node's unique sn to the type ('alt',
        'rep', or 'seq') of its parent."""
        raise NotImplemented
    
    def graph(self):
        """ Returns a list of parent-child pairs. Only the sequence
        number is given for each node.
        
            [(parent#, child#), ...]
        
        The order of child nodes for every Seq must be preserved. (And
        it is here, but only because of how it is implemented. I need
        to fix this.)
        """
        raise NotImplemented

    def labels(self):
        """A label is the user-given name of a node. Note that the
        name may be any text that the user provides, and is not
        resticted to looking like an identifier.

            [(node#, 'label'), ...]
        
        This function returns a list of node-label pairs. Each node is
        identified by its sequence number"""
        raise NotImplemented

    def walk(self, f=lambda x: x, level=0):
        yield f((level, self.sn, self.ntype, self.label, len(self.child)))
        for c in self.child:
            for t in c.walk(f=f, level=level+1):
                yield t

    def relabel(self,dict):
        try:
            self.label = dict[self.label]
        except KeyError:
            pass
        for c in self.child:
            c.relabel(dict)
            
    def parents(self):
        """ Return a set of node# that has every node that acts as
        parent somewhere."""
        return set(p for (p,_) in self.graph())
    
    def children_of(self, parent):
        """ Return a sequence (generator) of child# for the given
        parent#. """
        for (pp, child) in self.graph():
            if pp == parent:
                yield child
                
class Lit(Abstract):
    def __repr__(self): return '({} {})'.format(self.ntype,self.label)
    def graph(self): return []
    def labels(self): return [(self.sn, self.label)]
    def anno(self): return []
    def lisp(self): return '(lit %s)\n' % self.label

class Compound(Abstract):
    
    """
    Code to reuse by subclasses.
    """
    
    def __repr__(self):
        return '({} {} [{}])'.format(self.ntype,self.label,self.children())
    
    def add_child(self, other): self.child.append(other)

    def anno(self):
        r = []
        for c in self.child:
            r += c.anno()
            r.append((c.sn, self.ntype))
        return r
    
    def children(self): raise NotImplementedError
    
    def graph(self):
        r = []
        for c in self.child:
            r += c.graph()
            r.append((self.sn, c.sn))
        return r

    def labels(self):
        r = []
        r.append((self.sn, self.label))
        for c in self.child:
            r += c.labels()
        return r

class Rep(Compound):

    def __repr__(self):
        return '({} {} {})'.format(self.ntype,self.label,self.children())

    def add_child(self, other):
        assert self.child == [], "rep allows only one child"
        Compound.add_child(self,other)

    def children(self): return self.child[0]

class Rep1(Compound):

    def __repr__(self):
        return '({} {} {})'.format(self.ntype,self.label,self.children())

    def add_child(self, other):
        assert self.child == [], "rep allows only one child"
        Compound.add_child(self,other)

    def children(self): return self.child[0]

class Seq(Compound):

    def children(self): return ' '.join(repr(c) for c in self.child)

class Alt(Compound):

    def children(self): return ' '.join(repr(c) for c in self.child)

# TBD: do not use lisp syntax for repr()

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
    
if __name__ == '__main__':
    p = Lit('alpha')
    
    q = Seq('seq1')
    q.add_child(Lit('alpha'))
    q.add_child(Lit('beta'))
    q.add_child(Lit('gamma'))
    
    r = Alt('alt1')
    r.add_child(Lit('alpha'))
    r.add_child(Lit('beta'))
    r.add_child(Lit('gamma'))
    
    s = Rep('repX')
    s.add_child(Lit('alpha'))
    
    print p.labels()
    print q.labels()
    print r.labels()
    print s.labels()
    print '-' * 40
    print p.anno()
    print q.anno()
    print r.anno()
    print s.anno()
    print '-' * 40
    print p.graph()
    print q.graph()
    print r.graph()
    print s.graph()


'(alt alt1 [(lit alpha) (lit beta) (lit gamma)])'
'(rep repX (lit alpha))'
