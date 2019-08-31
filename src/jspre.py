#!python

# TBD: tree -> pydent

import argparse
import sys

import jsdtools.regex as regex
import jsdtools.lisp as lisp
import jsdtools.dot as dot
import jsdtools.pydent as pydent

"""
This script takes an argument string in jsp regex form. Stdin is not
read.

Depending on the --syntax option, The regex is translated to an
alternate syntax.

Example of Iterative Refinement
-------------------------------

(1) describe the lifetime of a single customer bank account with an
easy-to-type regular expression. The resulting python-like tree
('pydent') should be easy to read.

$ jspre.py '(invest . (pay-in | withdraw)* . terminate)'

 seq _3:
     invest
     rep _2:
         alt _1:
             pay-in
             withdraw
     terminate

(2) Supply more labels to replace the generated _1, _2 and _3.

To label some expression x, replace it with (x):my-label. It is a
little ugly, but easy to do with a little practice. For larger
structures, we can just write the 'pydent' form ourselves.

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
elaborations and finished with a pdf, all from the
command line. Not even a text editor was used.
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--syntax', default='tree')
    parser.add_argument('regex', nargs='+')
    args = parser.parse_args()
    
    asts = regex.parse_many(*args.regex)

    # Note: Parsing errors are reported late due to generator-based
    # lazy evaluation. I find this annoying.
    
    try:
        if args.syntax == 'tree':
            pydent.print_many(*asts)
        elif args.syntax == 'lisp':
            lisp.print_many(*asts)
        elif args.syntax == 'dot':
            dot.print_many(*asts)
        else:
            print ("bad syntax option: %r" % args.syntax, file=sys.stderr)
            sys.exit(-1)
    except regex.ParsingError as error:
        print ("bad parse: %r" % error, file=sys.stderr)
        sys.exit(-2)
