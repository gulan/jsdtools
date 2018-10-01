#!python

def side_by_side():
    """
    Accept a sequence of docs, where each doc is a list of
    strings. Print the docs side-by-side. The lines in each docs are
    right-padded with spaces. Each line in a padded docs will have the
    same width. Padded lines in the other docs will likely have
    different widths.

    Similarily, pad the bottom of each doc with blank lines so the all
    docs have the same height.
    """
    
    def bound_rects(doclist):
        # (high, wide) bounding rect of each doc
        for doc in doclist:
            pair = (len(doc), max(len(line) for line in doc))
            yield pair

    def fill(rects, docs):
        rects = list(rects)
        maxhigh = max(h for (h,_) in rects)
        for ((h,mw),d) in zip(rects, docs):
            d_ = [line.ljust(mw) for line in d]  # fill wide
            blank_lines = [' ' * mw] * (maxhigh - h)
            yield d_ + blank_lines               # fill high
        
    def _aux():
        docs = []
        while 1:
            try:
                doc = (yield)
            except GeneratorExit:
                break
            docs.append(doc)
                
        dlist = list(fill(bound_rects(docs), iter(docs)))
        for vec in zip(*dlist):
            print (' | '.join(vec))
    
    g = _aux()
    next(g)
    return g

def print_one(ast):
    raise NotImplementedError()

def print_many(*asts):
    
    def fmt(ast):
        for (level, _, node, name, _) in ast.walk():
            indent = '    ' * level
            if node == 'lit':
                line = indent + name
            else:
                line = indent + node + ' ' + name + ':'
            yield line
    
    g = side_by_side()
    for ast in asts:
        doc = list(fmt(ast))
        g.send(doc)
    g.close()
