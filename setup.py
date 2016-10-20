#!/usr/bin/env python

import sys
from setuptools import setup

setup(
    name='demandimport',
    version='0.3.3',
    description='On-demand imports, taken from mercurial',
    long_description="{0:s}\n{1:s}". format(
                    open('README.rst').read(),
                    open('CHANGES.rst').read()),
    author='Bas Westerbaan',
    author_email='bas@westerbaan.name',
    url='http://github.com/bwesterb/py-demandimport/',
    packages=['demandimport', 'demandimport.tests'],
    package_dir={'demandimport': 'src'},
    test_suite='demandimport.tests',
    license='GPLv2+',
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
            ]
    ),
