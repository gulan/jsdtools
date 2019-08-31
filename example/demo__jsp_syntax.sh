#!/bin/sh

PROG="python $HOME/1/jsd-tools/src/jsp_syntax.py"
RE='a . b* | (c . d)*'
echo "$RE" | $PROG -y regex -z regex >XXX1.regex
echo "$RE" | $PROG -y regex -z pydent >XXX1.pydent
echo "$RE" | $PROG -y regex -z lisp >XXX1.lisp
echo "$RE" | $PROG -y regex -z dot >XXX1.dot

cat XXX1.pydent | $PROG -y pydent -z regex  >XXX2.regex
cat XXX1.pydent | $PROG -y pydent -z pydent  >XXX2.pydent
cat XXX1.pydent | $PROG -y pydent -z lisp  >XXX2.lisp
cat XXX1.pydent | $PROG -y pydent -z dot  >XXX2.dot

cat XXX2.lisp | $PROG -y lisp -z regex  >XXX3.regex
cat XXX2.lisp | $PROG -y lisp -z pydent  >XXX3.pydent
cat XXX2.lisp | $PROG -y lisp -z lisp  >XXX3.lisp
cat XXX2.lisp | $PROG -y lisp -z dot  >XXX3.dot

if cmp XXX1.dot XXX2.dot; then echo OK; else echo BAD; fi
if cmp XXX1.regex XXX2.regex; then echo OK; else echo BAD; fi
if cmp XXX1.pydent XXX2.pydent; then echo OK; else echo BAD; fi
if cmp XXX1.lisp XXX2.lisp; then echo OK; else echo BAD; fi

# if cmp XXX1.dot XXX3.dot; then echo OK; else echo BAD; fi
# These dot files are isomorphic, but not identical. Why?
if cmp XXX1.regex XXX3.regex; then echo OK; else echo BAD; fi
if cmp XXX1.pydent XXX3.pydent; then echo OK; else echo BAD; fi
if cmp XXX1.lisp XXX3.lisp; then echo OK; else echo BAD; fi
