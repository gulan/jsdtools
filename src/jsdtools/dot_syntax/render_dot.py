#python

_subdict = {
    'rep': '*\\r',
    'rep1': '+\\r',
    'alt': 'o\\r',
    'seq': '.\\r',
    'lit': '',
    'root': ''}

def mkdot(target, cluster=False):
    # 'cluster' alters dot's layout behavior.
    def _aux():
        target.send('digraph fig7 {\n')
        target.send('  node [shape=rect]\n')
        target.send('  edge [dir=none]\n')
        ast_count = 1
        while 1:
            try:
                ast = (yield) # entire top-level AST in one slurp
            except GeneratorExit:
                break
            if cluster:
                t = '  subgraph cluster_compound%s {\n'
            else:
                t = '  subgraph compound%s {\n'
            target.send(t % ast_count)
            # nodes
            anno = dict(ast.anno())
            for (id, label) in ast.labels():
                prefix = _subdict[anno.get(id, 'root')]
                target.send('    {} [label="{}"]\n'.format(id, prefix+label))
            # edges
            for p in sorted(ast.parents()):
                chs = ' '.join(repr(c) for c in ast.children_of(p))
                target.send('    {} -> {}\n'.format(p, '{' + chs + '}'))
            target.send('  }\n')
            ast_count += 1
        target.send('}\n')
    x = _aux()
    next(x)
    return x

def mkprinter():
    def _aux():
        while 1:
            print ((yield), end='')
    printer = _aux()
    next(printer)
    return printer

def render_one(ast):
    dot = mkdot(mkprinter())
    dot.send(ast)
    dot.close()

