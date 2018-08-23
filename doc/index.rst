Welcome to the `sphinxcontrib-proof` documentation
==================================================

This `sphinx <http://sphinx.pocoo.org/>`__ extension provides some directives to
typeset theorems, proofs, etc. to both HTML and LaTeX builders.

Example
-------

.. proof:theorem:: Example

    A ``.. proof:theorem::`` statement produces a theorem.

.. proof:proof::

    And a ``.. proof:proof::`` statement produces a proof.

    This is self-explanatory.

Directive list
--------------

A statement is called using the ``.. proof:theorem`` (replacing ``theorem`` by
the statement name you want).

Available statements are:
``algorithm``,
``conjecture``,
``corollary``,
``definition``,
``example``,
``lemma``,
``observation``,
``proof``,
``property``,
``theorem``.
See section :ref:`usage` to learn how to add your custom labels.

If statement has an argument, it is considered to be the title of the
statement.


Download and install
--------------------

See the `main project page
<http://git.framasoft.org/spalax/sphinxcontrib-proof>`_ for instructions, and
`changelog
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/CHANGELOG.md>`_.

.. _usage:

Usage
-----

Add ``sphinxcontrib.proof`` to the list of sphinx extensions in your config
files, and use of the directives provided by this package.

Configuration options
"""""""""""""""""""""

* ``proof_theorem_labels`` : 

  List of theorems labels. Default is::

     proof_theorem_labels = {
        "algorithm": "Algorithm",
        "conjecture": "Conjecture",
        "corollary": "Corollary",
        "definition": "Definition",
        "example": "Example",
        "lemma": "Lemma",
        "observation": "Observation",
        "proof": "Proof",
        "property": "Property",
        "theorem": "Theorem",
     }

  Keys are the labels, as used in the directive (e.g. ``.. proof:LABEL::``) ; values are human readable labels.

  Modifying this list has two purposes:

  - adding new theorems;
  - translating labels (e.g. ``"proof": "Preuve",`` in French).

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``latex_proof_counter`` :

  For LaTeX documents, name of the section level at which the numbering is to take place. Default is ``latex_proof_counter = "chapter"``.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``latex_proof_main`` : 

  For LaTeX documents, name of the main theorem counter. All theorems share this counter (they are defined using ``\newtheorem{fancytheorem}[theorem]{My fancy theorem}``). Default is ``latex_proof_main = "theorem"``.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``latex_proof_notheorem`` : 

  For LaTeX documents, list of names of the directives that should not be defined (in LaTeX as theorems). See example below.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``latex_elements`` :

  Not specific to this extension, but you can add your custom theorem package in ``latex_elements['preamble']``. See example below.

Example
"""""""

For this documentation, I want the proofs not to be numbered. By default, LaTeX package ``amsthm`` ships with such a ``proof`` environment. Thus, my configuration file contains::

    latex_elements = {
        # Additional stuff for the LaTeX preamble.
        'preamble': r"""
            \usepackage{amsthm}
        """,
    }
    latex_proof_notheorem = ["proof"]

Line ``latex_proof_notheorem`` means: *"Define a Sphinx ``proof::proof`` directive, but do not define a LaTeX ``proof`` environment"*. The ``proof`` environment is defined in the ``amsthm`` LaTeX package, which is added to the preamble.

CSS and Javascript
------------------

HTML builder only add some html tags, but does not provides the CSS or
javascript that uses it. You can build your own, or use the one used by this
documentation package (`css
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/doc/_static/proof.css>`_
and `javascript
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/master/doc/_static/proof.js>`_)
by placing them into your documentation static directory.
Do not hotlink to those hosted here: they will change without notice.

