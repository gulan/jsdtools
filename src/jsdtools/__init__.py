#!python

import jsdtools.dot as dot
import jsdtools.lisp as lisp
import jsdtools.pydent as pydent
import jsdtools.regex as regex

"""
dot.print_many
dot.print_one

lisp.parse_many
lisp.parse_one
lisp.print_many
lisp.print_one

pydent.parse_many
pydent.parse_one
# pydent.print_many
pydent.print_one

regex.parse_many
regex.parse_one
# regex.print_many
regex.print_one
"""

def lisp_to_dot(x):
    dot.print_one(lisp.parse_one(x))
    
def lisp_to_lisp(x):
    lisp.print_one(lisp.parse_one(x))

def lisp_to_pydent(x):
    pydent.print_many(lisp.parse_one(x))
    
def lisp_to_regex(x):
    regex.print_one(lisp.parse_one(x))

def pydent_to_dot(x):
    dot.print_one(pydent.parse_one())

def pydent_to_lisp(x):
    lisp.print_one(pydent.parse_one())
    
def pydent_to_pydent(x):
    pydent.print_one(pydent.parse_one())

def pydent_to_regex(x):
    regex.print_one(pydent.parse_one())

def regex_to_dot(x):
    dot.print_one(regex.parse_one(x))
    
def regex_to_lisp(x):
    lisp.print_one(regex.parse_one(x))
    
def regex_to_pydent(x):
    pydent.print_one(regex.parse_one(x))

def regex_to_regex(x):
    regex.print_one(regex.parse_one(x))



# def lisp_to_dot(*x): dot.print_many(*lisp.parse_many(*x))
    
