#!python

import argparse
import sys
from jsdtools.regex_syntax.parse_re import RegexParser
from jsdtools.lisp_syntax.render_lisp import print_ast

"""
This script takes an argument string in jsp regex form. Stdin is not
read.

Depending on the --syntax option, The regex is translated to an
alternate syntax.

Since the regex form has no way to name non-leaf nodes of an ast, the
internal labels are, by default, generated.

These default labels may be replaced with explict labels provided with
the --label option.

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

$ jspre.py -l 'movement,activity,customer' '(invest . (pay-in | withdraw)* . terminate)'

 seq customer:
     invest
     rep activity:
         alt movement:
             pay-in
             withdraw
     terminate

(3) Looks good. So now convert the same expression into my standard ast form.

$ jspre.py -y lisp -l 'movement,activity,customer' '(invest . (pay-in | withdraw)* . terminate)' | tee out.jsd

(seq customer [
 (lit invest )
 (rep activity
  (alt movement [
   (lit pay-in   )
   (lit withdraw   )
  ])
 )
 (lit terminate )
])

(4) This saved out.jsp file can now be processed by astjsp.py to get a pdf.

$ astjsd.py <out.jsd |dot -T pdf -o out.pdf

Note how I started from scratch, performed a sequence of small
elaborations and finished with a nice pdf, all from the
command-line. Not even a text editor was used.


"""

def display_tree(r, subs):
    p = RegexParser()
    ast = p.parse(r)
    ast.relabel(subs)
    for (level, _, node, name, _) in ast.walk():
        if node == 'lit':
            print('    ' * level, name)
        else:
            print('    ' * level, node, name+':')
    return

def display_lisp(r, subs):
    p = RegexParser()
    ast = p.parse(r)
    ast.relabel(subs)
    print_ast(ast)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--labels', default='')
    parser.add_argument('-y', '--syntax', default='tree')
    parser.add_argument('regex')
    args = parser.parse_args()
    labels = args.labels.split(',')
    if labels[0] == '':
        subs = dict()
    else:
        keys = ["_%d" % i for i in range(1,len(labels)+1)]
        subs = dict(zip(keys, labels))
    if args.syntax == 'tree':
        display_tree(args.regex, subs)
    elif args.syntax == 'lisp':
        display_lisp(args.regex, subs)
    else:
        print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
        sys.exit(-1)
