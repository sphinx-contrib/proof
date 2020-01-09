.. _faq:

FAQ
===

.. contents::
   :local:
   :depth: 1

.. _latex-define-theorems:

How do I define LaTeX theorems?
-------------------------------

By default, this packages defines LaTeX theorems for you. Sometimes, this is not what you want. To disable this, you have to:

* set ``proof_latex_notheorem`` to the list of theorem types you want to define yourself (e.g. ``proof_latex_notheorem = ["definition", "theorem", "proof"]``);
* define those theorems (or environment) in ``latex_elements['preamble']``. For instance:

.. code-block:: python3

    latex_elements = {
        # Additional stuff for the LaTeX preamble.
        'preamble': r"""
           % My custom definition of environments definition, theorem, proof.
        """,
    }
    proof_latex_notheorem = ["definition", "theorem", "proof"]

.. _latex-unnumbered-proof:

LaTeX adds numbers to my proofs. How do I remove them?
------------------------------------------------------

Using the default configuration, LaTeX will number proofs (e.g. *Definition 1*, *Theorem 2*, *Proof 3*), which is probably not what you want.

To disable proof numbering with LaTeX, you have to :

* Add ``"proof"`` to ``proof_latex_notheorem``. Sphinx will define a ``proof::proof`` directive, but LaTeX will not define a ``proof`` environment.
* This ``proof`` environment has to be defined in ``latex_elements['preamble']``, either with your custom command, or by importing package `amsthm <https://www.ctan.org/pkg/amsthm>`__, which defines such a ``proof`` environment (which is not numbered).

The ``conf.py`` contains:

.. code-block:: python3

    latex_elements = {
        # Additional stuff for the LaTeX preamble.
        'preamble': r"""
            \usepackage{amsthm}
        """,
    }
    proof_latex_notheorem = ["proof"]

How to have different counters for definitions, theorems, etc.?
---------------------------------------------------------------

HTML
""""

You can't.

LaTeX
"""""

If option ``proof_latex_main`` is set to ``None``, definitions, theorems, properties, etc. will have different counters.

For more complex configuration (e.g. theorems and properties share a counter, but definitions do not), you have to define theorems yourself (see :ref:`latex-define-theorems`).

.. _numbered-theorems:

How to number theorems?
------------------------

HTML
""""

By default, theorems are not numbered. To number them, set ``numfig = True`` in the configuration file (see :ref:`html-numbering` to see advanced options).

LaTeX
"""""

By default, theorems are numbered. Nothing to configure here.

.. _unnumbered-theorems:

How not to number theorems?
----------------------------

In both cases, theorems cannot be referenced using ``:numref:``, but with ``:ref:``.

HTML
""""

Easy: in the configuration, use ``numfig = False`` (or do not define ``numfig``, which is ``False`` by default).

LaTeX
"""""

To disable theorem numbering, you have to define theorems yourself. That is:

* tell sphinx not to define theorem environments::

    proof_latex_notheorem = ["algorithm", "conjecture", "corollary", "definition", "example", "lemma", "observation", "proof", "property", "theorem"]

* define theorems in LaTeX, using the starred command (provided by `amsthm` or `ntheorem`)::

    latex_elements = {
        # Additional stuff for the LaTeX preamble.
        "preamble": r"""
           \usepackage{amsthm}

           \newtheorem*{definition}{Definition}
           \newtheorem*{theorem}{Theorem}
        """,
     }

.. _latex-numbering:

How to customize LaTeX numbering?
----------------------------------

LaTeX is great at counting stuff, and Sphinx do not intervene in this. To customize theorem numbering in LaTeX, you can:

* for simple cases, tweak options :ref:`proof_latex_main <proof_latex_main>` and :ref:`proof_latex_parent <proof_latex_parent>`;
* for complex cases, tell Sphinx not to define theorems (see entry :ref:`latex-define-theorems`) and define them yourself in configuration option :ref:`latex_elements <latex_elements>`.

Do you want some irrelevant theorems?
-------------------------------------

Here is an irrelevent theorem (`source <https://www.sciencedirect.com/science/article/pii/S1570868310000455>`__) to show that theorems can be referenced from the same page (:numref:`Theorem {number} <selfpromotion>`) or from other pages (:numref:`Theorem {number} <righttriangle>`).

.. _selfpromotion:

.. proof:theorem::

   #. If :math:`\Lambda` is a canonical modal logic, then the class of all frames that validate :math:`\Lambda` is quasimodal.
   #. A class of frames closed under the three fundamental frame constructions and ultraproducts is quasimodal.
   #. A modally definable elementary class of frames is quasimodal.

And here are others, without any label, or without title.

.. proof:theorem::

   Let :math:`\Lambda` be the modal logic of the quasimodal class K of frames, and let L be a class of frames containing K and having the same modal logic :math:`\Lambda`.

   #. K and L have the same hybrid logic.
   #. L is quasimodal

.. proof:corollary:: Non-quasimodal class of frames

   Let K be a class of frames, and :math:`\varphi` a hybrid formula valid in K. If :math:`\varphi` is not valid in the closure of K under the three fundamental operations and ultraroots, then K is not quasimodal.

.. _gammastar:

.. proof:conjecture:: Fake :math:`\Gamma^*` conjecture

   This is a dummy conjecture to illustrate that one can use math in theorem titles.

   Note that math typesetting is lost when referencing the theorem: :ref:`gammastar`.
