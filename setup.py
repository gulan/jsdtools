import sys
from setuptools import setup

NAME = 'jsd-tools'
DESCRIPTION = "Tools in support of M. Jackson's JSP/JSD development methods."
VERSION = '1.1.0'
AUTHOR = 'gulan'
AUTHOR_EMAIL = 'glen.wilder@gmail.com'

setup(name = NAME,
      version = VERSION,
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      description = DESCRIPTION,
      license = 'ISC',
      scripts = ['astjsd.py', 'spark7.py', 're2jsp'])

