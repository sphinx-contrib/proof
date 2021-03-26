Welcome to the `sphinxcontrib-proof` documentation
==================================================

This `sphinx <http://sphinx.pocoo.org/>`__ extension provides some directives to
typeset theorems, proofs, etc. to both HTML and LaTeX builders.

.. _simple:

Example
-------

Consider the following text.

  .. _righttriangle:

  .. proof:definition:: Right triangle
  
     A *right triangle* is a triangle in which one angle is a right angle.
  
  .. _pythagorean:

  .. proof:theorem:: Pythagorean theorem
  
     In a :ref:`righttriangle`, the square of the hypotenuse is equal to the sum of the squares of the other two sides.
  
  .. _proof:

  .. proof:proof::
  
     The proof is left to the reader.
  
  You can label and reference definition and theorems (e.g. :numref:`theorem {number} <pythagorean>`). You can also reference proofs (see the :ref:`proof of the Pythagorean theorem <proof>`).

To produce the above result, the following code was used (as well as `this CSS file <_static/proof.css>`__, and the :ref:`relevant configuration options <numbered-theorems>`).

.. code-block:: rst

  .. _righttriangle:

  .. proof:definition:: Right triangle
  
     A *right triangle* is a triangle in which one angle is a right angle.
  
  .. _pythagorean:

  .. proof:theorem:: Pythagorean theorem
  
     In a :ref:`righttriangle`, the square of the hypotenuse is equal to the sum of the squares of the other two sides.
  
  .. _proof:

  .. proof:proof::
  
     The proof is left to the reader.
  
  You can label and reference definition and theorems (e.g. :numref:`theorem {number} <pythagorean>`). You can also reference proofs (see the :ref:`proof of the Pythagorean theorem <proof>`).


Download and Install
--------------------

See the `main project page
<http://git.framasoft.org/spalax/sphinxcontrib-proof>`_ for instructions, and
`changelog
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/main/CHANGELOG.md>`_.

Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   usage
   faq

