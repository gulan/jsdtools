Generate Jackson Tree Diagrams from a DSL
=========================================

The lifetime activity of a single bank customer might be represented
as a regular expression. Given the events invest, pay-in, withdraw and
terminate, a regular expression constrains the possible orderings of
these events. ::

    invest + (payin | withdraw)* + terminate

Micheal Jackson's early work (1975) made no reference to regular
expressions, and recommended drawing tree diagrams instead. Each node
in the tree is either a sequence, an alternation, a repetition or a
symbol or literal terminal. Since the method requires that every node
in the tree have a name, nested regular expressions are not adequate. I
can rewrite the above using regular grammar as ::

    account ::= invest + activity + terminate
    activity ::= movement*
    movement ::= payin | withdraw

This BNF description lets me give a name to every subexpression, but
it is meant to describe full grammars, which are too powerful for my
needs. I do not want to put all names into the global scope and I do
not need recursive definitions.

To make my hand-written parser quick and easy to write, I started with
a very simple syntax based on LISP. The actual input to my program is
::

    (seq account [
        (lit invest)
        (rep activity
            (alt movement [
                (lit payin)
                (lit withdraw)]))
        (lit terminate)])

If the input file is `account.jsd`, the program from the command line
can be run as ::

    $ astjsd.py < account.jsd

This will write a Graphviz dot file to stdout, which may in turn be
used to create a graphic representation of the tree ::

    $ astjsd.py < account.jsd | dot -T pdf >account.pdf
    $ evince account.pdf &

.. image:: example/account/account.gif

The regular expression form of account.jsd can be recovered by ::

    $ astjsd.py -y regex <example/account/account.jsd 
    (invest . (payin | withdraw)* . terminate)

This regex form makes it easier to see the underlying structure. I can
also start with the regex syntax to build the LISP form ::

    $ jspre.py -y lisp \
      '(invest . ((payin | withdraw):movement*):activity . terminate):account'
   
    (seq account [
        (lit invest )
        (rep activity
        (alt movement [
            (lit payin)
            (lit withdraw)]))
    (lit terminate)])

    $ jspre.py -y dot \
      '(invest . ((payin|withdraw):movement*):activity . terminate):account' |\
      dot -Tpdf -o xxx.pdf    

See the docstring in jspre.py for details.

References
----------
| https://en.wikipedia.org/wiki/Michael_A._Jackson
| M.A. Jackson, "Principles of Program Design" Academic Press, 1975
| M.J. King and J.P. Pardoe, "Program Design Using JSP, A Practical Introduction", Macmillan Publishers LTD, 1985

