import sys
from os.path import (basename, dirname, splitext)
from glob import glob
from setuptools import (setup, find_packages)

NAME = 'jsd-tools'
DESCRIPTION = "Tools in support of M. Jackson's JSP/JSD development methods."
VERSION = '1.3.4'
AUTHOR = 'gulan'
AUTHOR_EMAIL = 'glen.wilder@gmail.com'

setup(name = NAME,
      version = VERSION,
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      description = DESCRIPTION,
      license = 'ISC',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      scripts = ['src/astjsd.py','src/jspre.py'])

