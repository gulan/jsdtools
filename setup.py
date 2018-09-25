import sys
from setuptools import (setup, find_packages)

with open("README.rst", "r") as fh:
    long_description = fh.read()
    
NAME = 'jsdtools'
DESCRIPTION = "Tools in support of M. Jackson's JSP/JSD development methods."
VERSION = '1.4.3'
AUTHOR = 'gulan'
AUTHOR_EMAIL = 'glen.wilder@gmail.com'

setup(name = NAME,
      version = VERSION,
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      description = DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url = 'https://github.com/gulan/jsdtools',
      license = 'ISC',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
#      python_requires='~=3.7',
      classifiers = [
          'Environment :: Console',
          'License :: OSI Approved :: ISC License (ISCL)',
          'Operating System :: POSIX',
#          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development'
      ],
      scripts = ['src/astjsd.py','src/jspre.py'])
