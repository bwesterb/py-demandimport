import unittest
import textwrap
import os.path
import sys

import demandimport
from demandimport.tests import TestModule

# Test-cases for bugs we encountered

import_hook = """
import sys
import importlib

class _LibImp(object):
    our_children = '{}.'.format(__package__)
    lib_module = '{}.lib'.format(__package__)
    lib_children = '{}.lib.'.format(__package__)

    @staticmethod
    def should_load(name):
        return name.startswith(_LibImp.our_children) and not (
            name == _LibImp.lib_module
            or name.startswith(_LibImp.lib_children)
        )

    def find_module(self, name, path=None):
        if self.should_load(name):
            return self
        return None

    def load_module(self, name):
        if name not in sys.modules:
            other_name = name
            if self.should_load(name):
                name = name.replace(
                    __package__,
                    '{}.lib'.format(__package__),
                    1)
            try:
                sys.modules[other_name] = importlib.import_module(name)
            except ImportError as e:
                raise ImportError(
                    'received request for {} but Unable to import {}: {}'
                    .format(other_name, name, e))
        return sys.modules[name]

sys.meta_path.append(_LibImp())
"""

class TestIssues(unittest.TestCase):
    def test_issue1(self):
        with TestModule() as m:
            with demandimport.enabled():
                with open(os.path.join(m.path, 'a.py'), 'w') as f:
                    f.write(textwrap.dedent("""
                            import {0}.b
                            {0}.b.__name__
                            """).format(m.name))
                with open(os.path.join(m.path, 'b.py'), 'w') as f:
                    pass
                __import__(m.name+'.a', locals={'foo': 'bar'}).a.__name__

    def test_issue2(self):
        with TestModule() as m:
            with demandimport.enabled():
                os.mkdir(os.path.join(m.path, 'a'))
                with open(os.path.join(m.path, 'a', '__init__.py'), 'w') as f:
                    pass
                with open(os.path.join(m.path, 'a', 'b.py'), 'w') as f:
                    pass
                __import__(m.name+'.a.b', locals={'foo': 'bar'}).a.b.__name__

    def test_issue3(self):
        if sys.version_info[0] >= 3:
            return
        with TestModule() as m:
            with demandimport.enabled():
                os.mkdir(os.path.join(m.path, 'a'))
                with open(os.path.join(m.path, 'a', '__init__.py'), 'w') as f:
                    pass
                with open(os.path.join(m.path, 'a', 'b.py'), 'w') as f:
                    pass
                with open(os.path.join(m.path, 'a', 'c.py'), 'w') as f:
                    f.write("from b import *")
                __import__(m.name+'.a.c', locals={'foo': 'bar'}).a.c.__name__

    def test_issue3_hook(self):
        with TestModule() as m:
            with open(os.path.join(m.path, '__init__.py'), 'a') as f:
                f.write(import_hook)
            os.mkdir(os.path.join(m.path, 'lib'))
            open(os.path.join(m.path, 'lib', '__init__.py'), 'w').close()
            open(os.path.join(m.path, 'lib', 'b.py'), 'w').close()
            with open(os.path.join(m.path, 'lib', 'c.py'), 'w') as f:
                f.write("import {}.b".format(m.name))
            __import__(m.name).__name__
            with demandimport.enabled():
                __import__(m.name+'.c',
                           locals={'foo': 'bar'},
                           level=0).c.__name__
                __import__(m.name+'.lib.c',
                           locals={'foo': 'bar'},
                           level=0).lib.c.__name__


if __name__ == '__main__':
    def log(msg, *args):
        print(msg % args)
    demandimport.set_logfunc(log)
    unittest.main()
