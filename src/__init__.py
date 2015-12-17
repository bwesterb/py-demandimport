# demandimport.py - global demand-loading of modules for Mercurial
#
# Copyright 2006, 2007 Matt Mackall <mpm@selenic.com>
#           2013, 2015 Bas Westerbaan <bas@westerbaan.name>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

'''
demandimport - automatic demandloading of modules

To enable this module, do:

  import demandimport; demandimport.enable()

Imports of the following forms will be demand-loaded:

  import a, b.c
  import a.b as c
  from a import b,c # a will be loaded immediately

These imports will not be delayed:

  from a import *
  b = __import__(a)
'''

from six.moves import builtins
_origimport = __import__
import pprint
import imp

class _demandmod(object):
    """module demand-loader and proxy"""
    def __init__(self, name, globals, locals, level=-1):
        global _ignore
        if '.' in name:
            head, rest = name.split('.', 1)
            after = [rest]
        else:
            head = name
            after = []
        object.__setattr__(self, "_data", (head, globals, locals, after, level))
        object.__setattr__(self, "_module", None)
        object.__setattr__(self, "_ignore", set(_ignore))
    def _extend(self, name):
        """add to the list of submodules to load"""
        self._data[3].append(name)
    def _load(self):
        if not self._module:
            global _ignore
            head, globals, locals, after, level = self._data
            if _log:
                if after:
                    _log('Triggered to import %s and setup lazy submodules %s '+
                            'for %s', head, after, globals.get('__name__', '?'))
                else:
                    _log('Triggered to import %s for %s', head,
                                    globals.get('__name__', '?'))
            old_ignore, _ignore = _ignore, self._ignore
            if level == -1:
                mod = _origimport(head, globals, locals)
            else:
                mod = _origimport(head, globals, locals, level)
            _ignore = old_ignore
            # load submodules
            def subload(mod, p):
                h, t = p, None
                if '.' in p:
                    h, t = p.split('.', 1)
                if not hasattr(mod, h):
                    if _log:
                        _log('Delaying import of %s for %s as %s situation #4',
                                p, mod.__dict__.get('__name__', '?'), h)
                    setattr(mod, h, _demandmod(p, mod.__dict__, mod.__dict__))
                elif t:
                    subload(getattr(mod, h), t)

            for x in after:
                subload(mod, x)

            # are we in the locals dictionary still?
            if locals and locals.get(head) == self:
                locals[head] = mod
            object.__setattr__(self, "_module", mod)

    def __repr__(self):
        if self._module:
            return "<proxied module '%s'>" % self._data[0]
        return "<unloaded module '%s'>" % self._data[0]
    def __call__(self, *args, **kwargs):
        raise TypeError("%s object is not callable" % repr(self))
    def __getattribute__(self, attr):
        if attr in ('_data', '_extend', '_load', '_module', '_ignore'):
            return object.__getattribute__(self, attr)
        self._load()
        return getattr(self._module, attr)
    def __setattr__(self, attr, val):
        self._load()
        setattr(self._module, attr, val)

def _demandimport(name, globals=None, locals=None, fromlist=None, level=-1):
    if not locals or name in _ignore or fromlist == ('*',):
        # these cases we can't really delay
        if level == -1:
            return _origimport(name, globals, locals, fromlist)
        else:
            return _origimport(name, globals, locals, fromlist, level)
    elif not fromlist:
        # import a [as b]
        if '.' in name: # a.b
            base, rest = name.split('.', 1)
            # email.__init__ loading email.mime
            if globals and globals.get('__name__', None) == base:
                if level != -1:
                    return _origimport(name, globals, locals, fromlist, level)
                else:
                    return _origimport(name, globals, locals, fromlist)
            # if a is already demand-loaded, add b to its submodule list
            if base in locals:
                if isinstance(locals[base], _demandmod):
                    if _log:
                        _log('Adding %s to submodule list of %s', rest, base)
                    locals[base]._extend(rest)
                return locals[base]
        else: # '.' not in name
            # For an absolute import of an unnested module, we can check
            # whether the module exists without loading anything.
            # So lets do that.
            if level == 0: # abs. import
                imp.find_module(name)
        if _log:
            _log('Delaying import of %s for %s (level %s) situation #1', name,
                            globals.get('__name__', '?'), level)
        return _demandmod(name, globals, locals, level)
    else:
        if level != -1:
            # from . import b,c,d or from .a import b,c,d
            return _origimport(name, globals, locals, fromlist, level)
        # from a import b,c,d
        mod = _origimport(name, globals, locals)
        # recurse down the module chain
        for comp in name.split('.')[1:]:
            if not hasattr(mod, comp):
                if _log:
                    _log('Delaying import of %s for %s situation #2',
                            comp, mods.get('__name__', '?'))
                setattr(mod, comp, _demandmod(comp, mod.__dict__, mod.__dict__))
            mod = getattr(mod, comp)
        for x in fromlist:
            # set requested submodules for demand load
            if not hasattr(mod, x):
                if _log:
                    _log('Delaying import of %s for %s situation #3', x,
                                    mod.__dict__.get('__name__', '?'))
                setattr(mod, x, _demandmod(x, mod.__dict__, locals))
                # This ensures
                #
                #    with demandimport.ignored('a.b.c'):
                #        from a.b import c
                #
                # behaves as expected.
                # TODO we should skip the `_demandmod'.
                if name + '.' + x in _ignore:
                    getattr(mod, x)._load()
        return mod

_ignore = set([
    '_hashlib',
    '_xmlplus',
    'fcntl',
    'win32com.gen_py',
    '_winreg', # 2.7 mimetypes needs immediate ImportError
    'pythoncom',
    # imported by tarfile, not available under Windows
    'pwd',
    'grp',
    # imported by profile, itself imported by hotshot.stats,
    # not available under Windows
    'resource',
    # this trips up many extension authors
    'gtk',
    # setuptools' pkg_resources.py expects "from __main__ import x" to
    # raise ImportError if x not defined
    '__main__',
    '_ssl', # conditional imports in the stdlib, issue1964
    ])

is_enabled = False
_log = None

def ignore(module_name):
    global _ignore
    _ignore.add(module_name)

class ignored(object):
    def __init__(self, module_name):
        self.module_name = module_name
    def __enter__(self):
        global _ignore
        self.added = self.module_name not in _ignore
        if self.added:
            _ignore.add(self.module_name)
    def __exit__(self, *args):
        global _ignore
        if self.added:
            _ignore.remove(self.module_name)

def enable():
    "enable global demand-loading of modules"
    global is_enabled
    if not is_enabled:
        builtins.__import__ = _demandimport
        is_enabled = True

def disable():
    "disable global demand-loading of modules"
    global is_enabled
    if is_enabled:
        builtins.__import__ = _origimport
        is_enabled = False

class disabled(object):
    def __enter__(self):
        global is_enabled
        self.old = is_enabled
        if is_enabled:
            disable()
    def __exit__(self, *args):
        if self.old:
            enable()

class enabled(object):
    def __enter__(self):
        global is_enabled
        self.old = is_enabled
        if not is_enabled:
            enable()
    def __exit__(self, *args):
        if not self.old:
            disable()

def set_logfunc(logfunc):
    """ Sets a logger to which demandimport will report all of its actions.

        Useful to debug problems with third-party modules. """
    global _log
    _log = logfunc
