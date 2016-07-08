demandimport
************

Delays loading of modules until they are actually used.  Perfect for Python
apps that need to be snappy like command-line utils.  Source-code derived
from mercurial.

To enable, write

.. code:: python

   import demandimport; demandimport.enable()

Imports of the following form will be delayed

.. code:: python

   import a, b.c
   import a.b as c
   from a import b, c # a will be loaded immediately, though

These imports with not be delayed

.. code:: python

   from a import *
   b = __import__(a)

Delayed loading will confuse some third-party modules.  In that case you
can disable the delay for just that module.  For example

.. code:: python

   demandimport.ignore('Crypto.PublicKey._fastmath')

There are also versions that can be used with ``with``

.. code:: python

   with demandimport.enabled():
      # do something
      with demandimport.disabled():
         import troublesome.module
      with demandimport.ignored('test'):
         import other.troublemaker

Installation
============

To install ``demandimport``, simply run::

   pip install demandimport

Attribution
===========

Matt Mackall <mpm@selenic.com> is the original author of the module in
Mercurial on which this module is based.  Bas Westerbaan <bas@westerbaan.name>
maintains it now.
