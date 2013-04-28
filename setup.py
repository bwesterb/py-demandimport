#!/usr/bin/env python

import sys
from setuptools import setup
from get_git_version import get_git_version

setup(
    name='demandimport',
    version=get_git_version(),
    description='On-demand imports, taken from mercurial',
    author='Bas Westerbaan',
    author_email='bas@westerbaan.name',
    url='http://github.com/bwesterb/py-demandimport/',
    packages=['demandimport'],
    package_dir={'demandimport': 'src'},
    license='GPL 2.0',
    ),
