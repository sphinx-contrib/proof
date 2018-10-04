.. _faq:

FAQ
===

.. contents::
   :local:
   :depth: 1

.. _latex-unnumbered-proof:

Unnumbered proof with LaTeX
---------------------------

Using the default configuration, LaTeX will number proofs (e.g. *Definition 1*, *Theorem 2*, *Proof 3*), which is probably not what you want.

To disable proof numbering with LaTeX, you have to :

* Add ``"proof"`` to ``latex_proof_notheorem``. Sphinx will define a ``proof::proof`` directive, but LaTeX will not define a ``proof`` environment".
* This ``proof`` environment has to be defined in ``latex_elements['preamble']``, either with your custom command, or by importing package `amsthm <https://www.ctan.org/pkg/amsthm>`__, which defines such a ``proof`` environment (which is not numbered).

The ``conf.py`` contains:

.. code-block:: python3

    latex_elements = {
        # Additional stuff for the LaTeX preamble.
        'preamble': r"""
            \usepackage{amsthm}
        """,
    }
    latex_proof_notheorem = ["proof"]

.. _unnumbered-theorems:

Unnumbered theorems
-------------------

In both cases, referencing theorems using ``:thm:`` will use a bogus theorem number. So, reference them using ``:thm:`my custom name <pythagorean>`` instead of ``:thm:`pythagorean```.

HTML
""""

Easy: in the configuration, use ``html_proof_number_theorems = False``.

LaTeX
"""""

To disable theorem numbering, you have to define theorems yourself. That is:

* tell sphinx not to define theorem environments::

    latex_proof_notheorem = ["algorithm", "conjecture", "corollary", "definition", "example", "lemma", "observation", "proof", "property", "theorem"]

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

Custom LaTeX numbering
----------------------

LaTeX is great at counting stuff, but by default, Sphinx is counting them instead. Allowing Sphinx to count and reference theorems with as many options as LaTeX would mean rewriting half of the Sphinx code in this package. I do not want to do or maintain this.

If you really want to use the power of LaTeX to count your theorems, take the :ref:`previous answer <unnumbered-theorems>` as an example, that is:

* tell sphinx not to define theorem environments::

    latex_proof_notheorem = ["algorithm", "conjecture", "corollary", "definition", "example", "lemma", "observation", "proof", "property", "theorem"]

* do whatever you want with LaTeX, using the ``latex_elements`` variable::

    latex_elements = {
        # Additional stuff for the LaTeX preamble.
        "preamble": r"""
           \usepackage{amsthm}

           % Complex stuff with theorems.
        """,
     }

Note that references to theorems use the Sphinx counter, which will be wrong in this case.

Another example
----------------

An irrelevent theorem (`source <https://www.sciencedirect.com/science/article/pii/S1570868310000455>`__) to show that theorems can be referenced from the same page (:thm:`self-promotion`) or from other pages (:thm:`right`).

.. proof:theorem::
  :label: self-promotion

   Let Λ be the modal logic of the quasimodal class K of frames, and let L be a class of frames containing K and having the same modal logic Λ.

   #. K and L have the same hybrid logic.
   #. L is quasimodal
