#!python

def side_by_side(target=None):
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
            line = ' | '.join(vec)
            if target:
                target.send(line)
            else:
                print(line)
    
    g = _aux()
    next(g)
    return g

def print_one(ast):
    print_many(ast)

def print_many(*asts):

    pg = []
    def page_buffer():
        while 1:
            try:
                line = (yield)
            except GeneratorExit:
                break
            pg.append(line)
            
    def fmt(ast):
        for (level, _, node, name, _) in ast.walk():
            indent = '    ' * level
            if node == 'lit':
                line = indent + name
            else:
                line = indent + node + ' ' + name + ':'
            yield line
    
    target = page_buffer()
    next(target)
    g = side_by_side(target=target)
    for ast in asts:
        doc = list(fmt(ast))
        g.send(doc)
    g.close()
    print ('\n'.join(pg))
