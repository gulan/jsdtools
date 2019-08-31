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

I chose a python-like syntax to represent the same regular expression.
::

    seq account:
        invest
        rep activity:
            alt movement:
                payin
                withdraw
        terminate

If this structure is in a file called `account.jsd`. A diagram may be
generated with
::

    $ jsp_syntax.py -y pydent -z dot < account.jsd >account.dot
    $ dot -T pdf >account.pdf
    $ evince account.pdf &

.. image:: example/account/account.gif

JSP is a method for designing sequential processes. In brief, the
steps are

1. Describe all input and output streams as regular expressions,
   biased towards the problem being solved.

2. Unify these regular expressions, if possible, resulting in the
   program structure. Unification is not possible when there is a
   structure clash. It may be resolved by implementing
   coroutines. (See references).

3. List the program statements in no particular order.

4. For each statement, find where it belongs in the program structure
   and attach it.

5. Convert the resulting program schema to real code.
           
Eventually, jsdtool will aid in steps 1-4. Currently it can only help
with step 1, but that is where is is most useful as creating the
diagrams by hand is tedious.
   
References
----------
| https://en.wikipedia.org/wiki/Michael_A._Jackson
| M.A. Jackson, "Principles of Program Design" Academic Press, 1975
| M.J. King and J.P. Pardoe, "Program Design Using JSP, A Practical Introduction", Macmillan Publishers LTD, 1985

