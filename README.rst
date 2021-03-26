`sphinxcontrib-proof` ∎ Typeset theorems, proofs, properties…
=============================================================

This `sphinx <http://sphinx.pocoo.org/>`__ extension provides some directives
to typeset theorems, properties, proofs, etc. You can see it in action in
`Jouets' documentation <http://jouets.readthedocs.io/fr/latest/dobble/math/>`_.

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/main/CHANGELOG.md>`_.

Install
-------

This module is compatible with python 3 only.

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/sphinxcontrib-proof
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

      python3 setup.py install

* From pip::

    pip install sphinxcontrib-proof

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/python3-sphinxcontrib-proof-<VERSION>_all.deb

Documentation
-------------

The documentation is available on `readthedocs <http://sphinxcontrib-proof.readthedocs.io>`_.  You can build it using::

  cd doc && make html
