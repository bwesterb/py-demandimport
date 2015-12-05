#!/usr/bin/env python

import sys
from setuptools import setup

setup(
    name='demandimport',
    version='0.2.2dev0',
    description='On-demand imports, taken from mercurial',
    long_description="{0:s}\n{0:s}". format(
                    open('README.rst').read(),
                    open('CHANGES.rst').read()),
    author='Bas Westerbaan',
    author_email='bas@westerbaan.name',
    url='http://github.com/bwesterb/py-demandimport/',
    packages=['demandimport'],
    package_dir={'demandimport': 'src'},
    license='GPL 2.0',
    ),
