#! /bin/sh

# original='(a*.d | g*)*'
original=$1
echo $original

alias regex-to-lisp="jspre.py -y lisp"
alias lisp-to-regex="astjsd.py -y regex"

equiv=$(regex-to-lisp "$original" | lisp-to-regex)  # 1
echo $equiv

same=$(regex-to-lisp "$equiv"     | lisp-to-regex) # 2
echo $same

# equiv's value means the same as original's, but the literal syntax
# differs in spacing and with redundant parenthesizes. So (1) is
# almost identity. The second time with (2), really is a literal
# identity.
