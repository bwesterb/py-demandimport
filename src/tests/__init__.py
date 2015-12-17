import os
import sys
import shutil
import random
import os.path
import textwrap
import tempfile

LOADED = set()

class TestModule(object):
    def __enter__(self):
        self.tempdir = tempfile.mkdtemp()
        self.name = 'testmodule{0}'.format(random.randint(0,2**128))
        sys.path.append(self.tempdir)
        self.path = os.path.join(self.tempdir, self.name)
        os.mkdir(self.path)
        with open(os.path.join(self.path, '__init__.py'), 'w') as f:
            f.write(textwrap.dedent('''
                        import demandimport.tests
                        name = {}
                        demandimport.tests.LOADED.add(name)
                        ''').format(repr(self.name)))
        return self

    @property
    def loaded(self):
        return self.name in LOADED

    def __exit__(self, *args):
        sys.path.remove(self.tempdir)
        shutil.rmtree(self.tempdir)
