Welcome to the `sphinxcontrib-proof` documentation
==================================================

This `sphinx <http://sphinx.pocoo.org/>`__ extension provides some directives to
typeset theorems, proofs, etc. to both HTML and LaTeX builders.

.. _simple:

Example
-------

Consider the following text.

  .. proof:definition::
     :label: right
  
     A *right triangle* is a triangle in which one angle is a right angle.
  
  .. proof:theorem:: Pythagorean theorem
     :label: pythagorean
  
     In a :thm:`right triangle <right>`, the square of the hypotenuse is equal to the sum of the squares of the other two sides.
  
  .. proof:proof::
  
     The proof is left to the reader.
  
  You can label and reference definition and theorems (e.g. :thm:`Pythagorean theorem <pythagorean>`, which is numbered as :thm:`pythagorean`).

To produce the above result, the following code was used (as well as `this CSS file <_static/proof.css>`__).

.. code-block:: rst

     .. proof:definition::
        :label: right
     
        A *right triangle* is a triangle in which one angle is a right angle.
     
     .. proof:theorem:: Pythagorean theorem
        :label: pythagorean
     
        In a :thm:`right triangle <right>`, the square of the hypotenuse is equal to the sum of the squares of the other two sides.
     
     .. proof:proof::
     
        The proof is left to the reader.
     
     You can label and reference definition and theorems (e.g. :thm:`Pythagorean theorem <pythagorean>`, which is numbered as :thm:`pythagorean`).


Download and Install
--------------------

See the `main project page
<http://git.framasoft.org/spalax/sphinxcontrib-proof>`_ for instructions, and
`changelog
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/CHANGELOG.md>`_.

Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   usage
   faq

