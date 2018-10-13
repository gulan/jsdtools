#!python

import sys

_subdict = {
    'rep': '*\\r',
    'rep1': '+\\r',
    'alt': 'o\\r',
    'seq': '.\\r',
    'lit': '',
    'root': ''}

def mkdot(target, cluster=False):
    # 'cluster' alters dot's layout behavior.
    """ mkdot return a coroutine that accepts any number of complete
    asts. When the source is closed, a single dot file for all ast
    trees is sent to the output.
    """
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

def mkprinter(out=sys.stdout):
    def _aux():
        while 1:
            print ((yield), end='')
    printer = _aux()
    next(printer)
    return printer

def print_one(ast):
    dot = mkdot(mkprinter())
    dot.send(ast)
    dot.close()

def print_many(*ast):
    dot = mkdot(mkprinter())
    for a in ast:
        dot.send(a)
    dot.close()

