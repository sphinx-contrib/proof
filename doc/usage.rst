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
the statement name you want). For instance, de define a right triangle, one might use:

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

Label and References
--------------------

.. warning::

   LaTeX and Sphinx use different counters. Theorems are labelled using the LaTeX counter, but referenced using the Sphinx counters. By default, those are the same. But if you mess with LaTeX theorem counters (for instance, if you want theorem numbers to go back to zero at each new chapter), references will be wrong.

Numbered theorems can be labeled using a ``:label:`` argument.

.. code-block:: rst

  .. proof:definition::
     :label: righttriangle

     A *right triangle* is a triangle in which one angle is a right angle.

Later on, they can be referenced:

* Sphinx code ``See :thm:`righttriangle`.`` will produce a link to the above definition, with text ``See Definition 1``.
* Sphinx code ``See the :thm:`right triangle definition <righttriangle>.``` will produce the same link, with custom text ``See the right triangle definition``.

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

.. _proof_unnumbered_types:

* ``proof_unnumbered_types`` :

  List of theorem types that are not numbered. Default is ``["proof"]``. Note that theorems of an unnumbered type cannot be referenced (using plop).


  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``proof_ref_format`` :

  Format string (as in `Python string formatting <https://docs.python.org/3/library/stdtypes.html#str.format>`_) used when referencing theorems. Defined variables are:

  - ``thmtype``: type of the theorem (Theorem, Proof, or any of the *values* of configuration option :ref:`proof_theorem_types <proof_theorem_types>`);
  - ``number``: number of the theorem.

  Note that:

  - Default value ``{thmtype} {number}`` will use a capital letter (unless you have removed them in :ref:`proof_theorem_types <proof_theorem_types>`). For instance (notice the capital letter which should not be here):

      We can now prove that :math:`x=1` by using :thm:`Theorem 1 <pythagorean>`.

  - Value ``{number}`` will not include the capital letter, but it is your job to add the theorem title, and you will get (notice the tiny link):

      We can now prove that :math:`x=1` by using theorem :thm:`1 <pythagorean>`.

  I am not sure one of them is better than the other one…

  .. versionchanged:: 1.1.0
     New in version 1.1.0.


HTML options
""""""""""""

* ``html_proof_title_template`` :

  Template used when labeling theorems. Default is:

  .. code-block:: html

      <div class="proof-title">
          <span class="proof-type">{{ thmtype }} {% if number %}{{number}}{% endif %}</span>
          {% if title %}
          <span class="proof-title-name">({{ title }})</span>
          {% endif %}
      </div>

  This is a `jinja2 template <http://jinja.pocoo.org/docs/2.10/templates/>`_, with available variables being:

  - ``thmtype``: type of the theorem (Theorem, Proof, or any of the *values* of configuration option :ref:`proof_theorem_types <proof_theorem_types>`);
  - ``number``: theorem number (``None`` if unnumbered);
  - ``title``: theorem title (``None`` if anonymous).

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``html_proof_number_theorems`` :

  `HTML` only. If ``False``, theorems are not numbered; if ``True``, theorems are numbered, excepted for types listed in :ref:`proof_unnumbered_types <proof_unnumbered_types>`.

  Theorems can still be referenced, but if you do not provide custom text (e.g. if you use ``:thm:`pythagorean`` instead of ``:thm:`Pythagorean theorem <pythagorean>``), the reference will display a bogus theorem number.

  To use unnumbered theorems in LaTeX, see :ref:`unnumbered-theorems`.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.


LaTeX options
"""""""""""""

* ``latex_proof_main`` :

  For LaTeX documents, name of the main theorem counter. All theorems share this counter (they are defined using ``\newtheorem{fancytheorem}[theorem]{My fancy theorem}``). Default is ``latex_proof_main = "theorem"``.

  More about LaTeX numbering can be found :ref:`in the FAQ <latex-numbering>`.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``latex_proof_notheorem`` :

  For LaTeX documents, list of names of the directives that should not be defined (in LaTeX as theorems). Default is empty.
 
 This option can be used to :ref:`have unnumbered proofs <latex-unnumbered-proof>`.

  .. versionchanged:: 1.1.0
     New in version 1.1.0.

* ``latex_proof_parent`` :

  Name of the parent counter, if any. Default is ``None``.

  For instance, if ``latex_proof_parent = "chapter"``, theorem counters will go back to zero at each new chapter.

  .. warning::

     LaTeX and Sphinx use different counters. Setting ``latex_proof_parent`` to anything else than the default will (probably) mean that numbers of references will be wrong (e.g. sphinx code ``see :thm:`pythagorean``` will display ``see Theorem 2``, although theorem is numbered ``Theorem 3.2``).

  .. versionchanged:: 1.1.0
     New in version 1.1.0.


* ``latex_elements`` :

  Not specific to this extension, but you can add your custom theorem package in ``latex_elements['preamble']``. See for instance this :ref:`FAQ entry <latex-unnumbered-proof>`.

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
