#!python

import argparse
import sys
from jsdtools.regex.parse import RegexParser
from jsdtools.lisp.render import print_ast
from jsdtools.dot.render import mkdot, mkprinter

"""
This script takes an argument string in jsp regex form. Stdin is not
read.

Depending on the --syntax option, The regex is translated to an
alternate syntax.

Example of Iterative Refinement
-------------------------------

(1) describe the lifetime of a single customer bank account with an
easy-to-type regular expression. The resulting python-like tree
should be easy to read.

$ jspre.py '(invest . (pay-in | withdraw)* . terminate)'

 seq _3:
     invest
     rep _2:
         alt _1:
             pay-in
             withdraw
     terminate

(2) Supply more labels to replace the generated _1, _2 and _3.

$ jspre.py '(invest . ((pay-in | withdraw):movement*):activity . terminate):customer'

 seq customer:
     invest
     rep activity:
         alt movement:
             pay-in
             withdraw
     terminate

(3) Looks good. So now convert the same expression graphviz dot language.

$ jspre.py -y dot '(invest . ((pay-in | withdraw):movement*):activity . terminate):customer'

digraph fig7 {
  node [shape=rect]
  edge [dir=none]
  subgraph compound1 {
    16 [label="customer"]
    10 [label=".\rinvest"]
    14 [label=".\ractivity"]
    13 [label="*\rmovement"]
    11 [label="o\rpay-in"]
    12 [label="o\rwithdraw"]
    15 [label=".\rterminate"]
    13 -> {11 12}
    14 -> {13}
    16 -> {10 14 15}
  }
}

(4) The output can be piped into dot to get a pdf.

$ jspre.py -y dot ... |dot -T pdf -o customer.pdf

Note how I started from scratch, performed a sequence of small
elaborations and finished with a nice pdf, all from the
command-line. Not even a text editor was used.
"""

def side_by_side():
    def _aux():
        doclist = []
        margins = []
        while 1:
            try:
                doc = (yield)
            except GeneratorExit:
                break
            doclist.append(doc)
            maxlen = max(len(m) for m in doc)
            margins.append(maxlen)

        maxhigh = max(len(m) for m in doclist)
            
        doclist1 = []
        for (inx,doc) in enumerate(doclist):
            m = margins[inx]
            doc1 = []
            for line in doc:
                doc1.append(line.ljust(m))
            short = maxhigh - len(doc)
            for _ in range(short):
                doc1.append(''.ljust(m))
            doclist1.append(doc1)
            
        for vec in zip(*doclist1):
            print (' | '.join(vec))

    g = _aux()
    next(g)
    return g

def display_tree(rs, subs):
    outputs = []
    g = side_by_side()
    p = RegexParser()
    for r in rs:
        doc = []
        ast = p.parse(r,subs)
        for (level, _, node, name, _) in ast.walk():
            indent = '    ' * level
            if node == 'lit':
                line = indent + name
            else:
                line = indent + node + ' ' + name + ':'
            doc.append(line)
        g.send(doc)
    g.close()
    return

def display_lisp(rs, subs):
    p = RegexParser()
    for r in rs:
        ast = p.parse(r,subs)
        print_ast(ast)
    return

def display_dot(rs, subs):
    dot = mkdot(mkprinter())
    p = RegexParser()
    for r in rs:
        ast = p.parse(r)
        ast.relabel(subs)
        dot.send(ast)
    dot.close()
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('-l', '--labels', default='')
    parser.add_argument('-y', '--syntax', default='tree')
    parser.add_argument('regex', nargs='+')
    args = parser.parse_args()
    # labels = args.labels.split(',')
    # if labels[0] == '':
    #     subs = dict()
    # else:
    #     keys = ["_%d" % i for i in range(1,len(labels)+1)]
    #     subs = dict(zip(keys, labels))
    subs = dict()
    if args.syntax == 'tree':
        display_tree(args.regex, subs)
    elif args.syntax == 'lisp':
        display_lisp(args.regex, subs)
    elif args.syntax == 'dot':
        display_dot(args.regex, subs)
    else:
        print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
        sys.exit(-1)
