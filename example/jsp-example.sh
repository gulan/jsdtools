#! /bin/sh

JSPRE="jspre.py -y lisp"
DOT="dot -T pdf -o "

$JSPRE -l 'repeat-iter,run,run-iter' '(first-byte . repeated-byte*)*' | astjsd.py | $DOT run-length-in.pdf
