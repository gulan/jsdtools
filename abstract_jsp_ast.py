#!/usr/bin/python

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
    
    def __init__(self,label):
        self.child = []
        self.label = label
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
        
        The order of child nodes for every Seq must be preserved. (And
        it is here, but only because of how it is implemented. I need
        to fix this.)
        """
        raise NotImplemented

    def labels(self):
        """A label is the user-given name of a node. Note that the
        name may be any text that the user provides, and is not
        resticted to looking like an identifier.
        
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
        return set(p for (p,_) in self.graph())
    
    def children_of(self, parent):
        for (pp, child) in self.graph():
            if pp == parent:
                yield child
                
class Lit(Abstract):
    def __repr__(self): return '({} {})'.format(self.ntype,self.label)
    def graph(self): return []
    def labels(self): return [(self.sn, self.label)]
    def anno(self): return []

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

