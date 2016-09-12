import sys
from setuptools import setup

NAME = "jsp-tooling"
DESCRIPTION = "Tools in support of M. Jackson's JSP/JSD development methods."
VERSION = "0.1.0"
AUTHOR = "gulan"
AUTHOR_EMAIL = "glen.wilder@gmail.com"

setup(name = NAME,
      version = VERSION,
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      description = DESCRIPTION,
      # packages = ['exile', 'test'],
      # test_suite = 'test.test_action',
      scripts = ['astjsd.py', 'runlen.py'])

