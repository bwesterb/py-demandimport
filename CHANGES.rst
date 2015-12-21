py-demandimport Changelog
*************************

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
