#!/usr/bin/env python
from distutils.core import setup
import os
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from pykwiki import __version__

setup(name='pykwiki',
    version = __version__,
    description = 'A simple pure-python wiki engine.',
    long_description = '''
A pure-python, light-weight, static wiki, blog, website engine designed for speed. 
    ''',
    author = 'Aaron Meier',
    author_email = 'webgovernor@gmail.com',
    packages = ['pykwiki','pykwiki.ext'],
    package_dir={'pykwiki':'pykwiki'},
    scripts=['pykwiki/scripts/pykwiki'],
    package_data={'pykwiki':['data/*.zip']},
    url = 'http://pykwiki.nullism.com',
    license = 'MIT',
    requires = ['markdown (>=2.3)', 'jinja2 (>=2.6)', 'pyyaml (>=3.0)'],
    provides = ['pykwiki']
)

