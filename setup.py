#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from pykwiki2 import __version__

setup(name='pykwiki2',
    version = __version__,
    description = 'A simple pure-python wiki engine.',
    long_description = '''
A pure-python, light-weight, static wiki, blog, and website engine designed to be
fast to setup, secure, and to handle lots of web traffic.
    ''',
    author = 'Aaron Meier',
    author_email = 'webgovernor@gmail.com',
    packages = ['pykwiki2','pykwiki2.ext'],
    package_dir={'pykwiki2':'pykwiki2'},
    scripts=['pykwiki2/scripts/pykwiki2'],
    package_data={
        'pykwiki2':[
            'data/*.zip',
            'data/default_data/*.yaml',
            'data/default_data/source/*.md',
            'data/default_data/styles/*/*.yaml',
            'data/default_data/styles/*/*.scss',
            'data/default_data/styles/*/static/*.*',
            'data/default_theme/*.html',
            'data/default_theme/*.xml',
            'data/default_theme/static/*.js',
            'data/default_theme/static/mustachejs/*.js',
            'data/default_theme/static/codehilite/*.css',
            'data/default_theme/static/fonts/*.css',
            'data/default_theme/static/fonts/*.ttf',
        ]},
    url = 'http://pykwiki.nullism.com',
    license = 'MIT',
    install_requires = ['markdown>=2.6', 'jinja2>=2.6', 'pyyaml>=3.0', 'pyscss>=1.3.4'],
    provides = ['pykwiki2']
)

