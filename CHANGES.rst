py-demandimport Changelog
*************************

0.3.4 (2017-06-08)
==================

- Python 3.6
- Add sip to the default ignore list.  #6


0.3.3 (2016-10-20)
==================

- Add ``is_loaded`` and ``is_proxy``.
  Thanks-to: github.com/poke1024


0.3.2 (2015-12-22)
==================

- Fixed issue #2: ``import a.b.c`` will incorrectly try to import ``b.c``


0.3.1 (2015-12-21)
==================

- Relicense GPL version 2 or later (GPLv2+)


0.3.0 (2015-12-21)
==================

- Do not delay ImportError in a special case.
- Add optional logging (for debugging)
- Fixed issue #1: ``import a.b`` in a module ``a.c`` was incorrectly executed
  as a relative ``import c``.
- Improve thread safety


0.2.2 (2015-12-05)
==================

- Moved to zest.releaser
- Add some basic unittests
- Python 3 support
