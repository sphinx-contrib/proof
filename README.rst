Description of the `sphinxcontrib-proof` Sphinx Extension
=========================================================

|sources| |pypi| |build| |coverage| |documentation| |license|

This `sphinx <http://sphinx.pocoo.org/>`__ extension provides some directives
to typeset theorems, properties, proofs, etc. You can see it in action in
`Jouets' documentation <http://jouets.readthedocs.io/fr/latest/dobble/math/>`_.

What's new?
-----------

See `changelog
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/CHANGELOG.md>`_.

Install
-------

This module is compatible with both python 2 and 3.

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/sphinxcontrib-proof
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

      python setup.py install

* From pip::

    pip install sphinxcontrib-proof

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/python3-sphinxcontrib-proof-<VERSION>_all.deb

Documentation
-------------

The documentation is available on `readthedocs
<http://sphinxcontrib-proof.readthedocs.io>`_.  You can build it using::

  cd doc && make html

.. |documentation| image:: http://readthedocs.org/projects/sphinxcontrib-proof/badge
  :target: http://sphinxcontrib-proof.readthedocs.io
.. |pypi| image:: https://img.shields.io/pypi/v/sphinxcontrib-proof.svg
  :target: http://pypi.python.org/pypi/sphinxcontrib-proof
.. |license| image:: https://img.shields.io/pypi/l/sphinxcontrib-proof.svg
  :target: http://www.gnu.org/licenses/agpl-3.0.html
.. |sources| image:: https://img.shields.io/badge/sources-sphinxcontrib--proof-brightgreen.svg
  :target: http://git.framasoft.org/spalax/sphinxcontrib-proof
.. |coverage| image:: https://framagit.org/spalax/sphinxcontrib-proof/badges/master/coverage.svg
  :target: https://framagit.org/spalax/sphinxcontrib-proof/builds
.. |build| image:: https://framagit.org/spalax/sphinxcontrib-proof/badges/master/build.svg
  :target: https://framagit.org/spalax/sphinxcontrib-proof/builds
