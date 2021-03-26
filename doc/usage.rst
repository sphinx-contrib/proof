Usage
=====

.. contents::
   :local:

Examples
--------

The main page includes a :ref:`simple example <simple>`.  More complex ones can be found in the :ref:`FAQ <faq>`.

Load extension
--------------

Add ``sphinxcontrib.proof`` to the list of sphinx extensions in your config
files, and use of the directives provided by this package.

In your `conf.py` file, have::

   extensions = ["sphinxcontrib.proof"]

Directive list
--------------

A statement is called using the ``.. proof:theorem`` (replacing ``theorem`` by
the statement name you want). For instance, to define a right triangle, one might use:

.. code-block:: rst

  .. proof:definition:: Right triangle

     A *right triangle* is a triangle in which one angle is a right angle.

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
See configuration option :ref:`proof_theorem_types <proof_theorem_types>` to learn how to add your custom types.

If statement has an argument, it is considered to be the title of the
statement.

.. _labels-references:

Labels and References
---------------------

Theorems can be labelled and referenced.

Unnumbered theorems
"""""""""""""""""""

Theorems that are not numbered can be labelled and referenced using the same tools used elsewhere in Sphinx; see: :ref:`ref-role`.

Numbered theorems
"""""""""""""""""

Numbered theorems are labelled, and can be referenced, using the same tools as the unnumbered theorems (see above paragraph). If ``numfig`` is true, they can also be referenced using ``:numref:`` (see :ref:`html-numbering` and `the sphinx documentation <http://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#role-numref>`__).

Configuration options
---------------------

Those options may be set in the ``conf.py`` file.

Common options
""""""""""""""

.. _proof_theorem_types:

* ``proof_theorem_types`` :

  List of theorems types. Default is::

     proof_theorem_types = {
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

  Keys are the types, as used in the directive (e.g. ``.. proof:TYPE::``) ; values are human readable types.

  Modifying this list has two purposes:

  - adding new theorems;
  - translating types (e.g. ``"proof": "Preuve",`` in French).

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

HTML options
""""""""""""

* ``proof_html_title_template_visit`` and ``proof_html_title_template_depart`` :

  Templates used when labeling theorems. Default are:

  - for ``proof_html_title_template_visit``:

      .. code-block:: html

         <div class="proof-title">
             <span class="proof-type">{{ thmtype }} {% if number %}{{number}}{% endif %}</span>
             {% if title %}
                 <span class="proof-title-name">(
             {%- endif -%}

  - for ``proof_html_title_template_depart``:

      .. code-block:: html

             {%- if title -%}
                 )</span>
             {% endif %}
         </div>

  Note that to build the title, one has to concat : ``proof_html_title_template_visit`` + *Optional theorem title* + ``proof_html_title_template_depart``.

  Those are `jinja2 templates <http://jinja.pocoo.org/docs/2.10/templates/>`_, with available variables being:

  - ``thmtype``: type of the theorem (Theorem, Proof, or any of the *values* of configuration option :ref:`proof_theorem_types <proof_theorem_types>`);
  - ``number``: theorem number (``None`` if unnumbered);
  - ``title``: boolean (``False`` if anonymous).

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

  .. versionchanged:: 1.2.0
     Split old ``proof_html_title_template`` into ``proof_html_title_template_visit`` and ``proof_html_title_template_depart``.


.. _proof_html_nonumbers:

* ``proof_html_nonumbers`` :

  List of theorem types that are not numbered. Default is ``["proof"]``. Note that theorems of an unnumbered type cannot be referenced using ``:numref:`` (but can be referenced with ``:ref:``).


  .. versionchanged:: 1.1.0
     New in version 1.1.0.

.. _html-numbering:

HTML numbering
""""""""""""""

HTML numbering can be configured using `numfig <http://www.sphinx-doc.org/en/master/usage/configuration.html#confval-numfig>`__, `numfig_format <http://www.sphinx-doc.org/en/master/usage/configuration.html#confval-numfig_format>`__, and `numfig_secnum_format <http://www.sphinx-doc.org/en/master/usage/configuration.html#confval-numfig_secnum_depth>`__.

Note that using ``:numref:`pythagorean``` will produce :numref:`pythagorean` (instead of :numref:`Theorem {number} <pythagorean>`). This is because although the counter is shared between definitions, theorems, etc., one *have to* share the same ``numref_format`` option (which is set to ``Proof %s`` by default) [#numrefpatch]_.

As a workaround, you can use ``:numref:`Theorem {number} <pythagorean>``` to produce :numref:`Theorem {number} <pythagorean>`.

.. versionchanged:: 1.1.0
  New in version 1.1.0.

LaTeX options
"""""""""""""

.. _proof_latex_main:

* ``proof_latex_main`` :

  For LaTeX documents, name of the main theorem counter. All theorems share this counter (they are defined using ``\newtheorem{fancytheorem}[theorem]{My fancy theorem}``). Default is ``proof_latex_main = "theorem"``.

  More about LaTeX numbering can be found :ref:`in the FAQ <latex-numbering>`.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``proof_latex_notheorem`` :

  For LaTeX documents, list of names of the directives that should not be defined (in LaTeX as theorems). Default is empty. You have to define those environment in :ref:`latex_elements <latex_elements>`, otherwise, LaTeX compilation will fail.
 
 This option is used to :ref:`have unnumbered proofs <latex-unnumbered-proof>`.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

.. _proof_latex_parent:

* ``proof_latex_parent`` :

  Name of the parent counter, if any. Default is ``None``.

  For instance, if ``proof_latex_parent = "chapter"``, theorem counters will go back to zero at each new chapter.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

.. _latex_elements:

* ``latex_elements`` :

  Not specific to this extension, but you can add your custom theorem package in ``latex_elements['preamble']``. See for instance this :ref:`FAQ entry <latex-unnumbered-proof>`.

CSS and Javascript
------------------

HTML builder only add some html tags, but does not provides the CSS or
javascript that uses it. You can build your own, or use the one used by this
documentation package (`css
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/main/doc/_static/proof.css>`_
and `javascript
<https://git.framasoft.org/spalax/sphinxcontrib-proof/blob/main/doc/_static/proof.js>`_)
by placing them into your documentation static directory.
Do not hotlink to those hosted here: they will change without notice.

.. rubric:: Footnotes

.. [#numrefpatch] To solve this, I could:

   - fork Sphinx;
   - rewrite half on Sphinx in my extension;
   - propose a patch to the official Sphinx project.

   For obvious reasons, I won't implement the first two solutions. I might try to implement the last one, but it will take time.

