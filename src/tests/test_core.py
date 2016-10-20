import unittest

import demandimport
from demandimport.tests import TestModule

class TestCore(unittest.TestCase):
    def test_enabled_property(self):
        self.assertFalse(demandimport.is_enabled)
        try:
            demandimport.enable()
            self.assertTrue(demandimport.is_enabled)
        finally:
            demandimport.disable()
        self.assertFalse(demandimport.is_enabled)

    def test_enabled_context(self):
        self.assertFalse(demandimport.is_enabled)
        with demandimport.enabled():
            self.assertTrue(demandimport.is_enabled)
        self.assertFalse(demandimport.is_enabled)

    def test_disabled_context(self):
        self.assertFalse(demandimport.is_enabled)
        with demandimport.enabled():
            self.assertTrue(demandimport.is_enabled)
            with demandimport.disabled():
                self.assertFalse(demandimport.is_enabled)
            self.assertTrue(demandimport.is_enabled)
        self.assertFalse(demandimport.is_enabled)

    def test_testmodule(self):
        with TestModule() as m:
            self.assertFalse(m.loaded)
            __import__(m.name)
            self.assertTrue(m.loaded)

    def test_ignoring__import__(self):
        with TestModule() as m:
            self.assertFalse(m.loaded)
            with demandimport.enabled():
                __import__(m.name)
                self.assertTrue(m.loaded)

    def test_simple(self):
        with TestModule() as m:
            self.assertFalse(m.loaded)
            with demandimport.enabled():
                lm = __import__(m.name, locals={'foo': 'bar'})
                self.assertFalse(m.loaded)
                self.assertEqual(lm.name, m.name)
                self.assertTrue(m.loaded)

    def test_ignoring_star(self):
        with TestModule() as m:
            self.assertFalse(m.loaded)
            with demandimport.enabled():
                __import__(m.name, locals={'foo': 'bar'}, fromlist=('*',))
                self.assertTrue(m.loaded)

    def test_ignore(self):
        with TestModule() as m:
            self.assertFalse(m.loaded)
            with demandimport.enabled():
                demandimport.ignore(m.name)
                lm = __import__(m.name, locals={'foo': 'bar'})
                self.assertTrue(m.loaded)

    def test_ignored(self):
        with TestModule() as m:
            self.assertFalse(m.loaded)
            with demandimport.enabled():
                with demandimport.ignored(m.name):
                    lm = __import__(m.name, locals={'foo': 'bar'})
                    self.assertTrue(m.loaded)

    def test_is_proxy_and_loaded(self):
        with TestModule() as m:
            lm = __import__(m.name)
            self.assertFalse(demandimport.is_proxy(lm))
            self.assertTrue(m.loaded)
            self.assertTrue(demandimport.is_loaded(lm))
        with TestModule() as m:
            with demandimport.enabled():
                lm = __import__(m.name, locals={'foo': 'bar'})
                self.assertTrue(demandimport.is_proxy(lm))
                self.assertFalse(demandimport.is_loaded(lm))
                self.assertFalse(m.loaded)
                self.assertEqual(lm.name, m.name)
                self.assertTrue(demandimport.is_loaded(lm))
                self.assertTrue(m.loaded)
                self.assertTrue(demandimport.is_proxy(lm))

if __name__ == '__main__':
    unittest.main()
