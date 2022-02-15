# Copyright 2015-2022 Louis Paternault
#
# Sphinxcontrib-Proof is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sphinxcontrib-Proof is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sphinxcontrib-Proof.  If not, see <http://www.gnu.org/licenses/>.

"""Provide tools to typeset theorems, proofs, etc. in Sphinx documentation."""

import logging
import os

import jinja2
from docutils import nodes
from docutils.nodes import make_id
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.domains import ObjType
from sphinx.domains.std import StandardDomain
from sphinx.roles import XRefRole
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import clean_astext, make_refnode, set_source_info

VERSION = "1.4.0"

################################################################################
# Configuration
PROOF_THEOREM_TYPES = {
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

PROOF_HTML_NONUMBERS = ["proof"]

PROOF_HTML_TITLE_TEMPLATE_VISIT = """
    <div class="proof-title">
        <span class="proof-type">{{ thmtype }} {% if number %}{{number}}{% endif %}</span>
        {% if title %}
            <span class="proof-title-name">(
        {%- endif -%}
"""

PROOF_HTML_TITLE_TEMPLATE_DEPART = """
        {%- if title -%}
            )</span>
        {% endif %}
    </div>
"""


################################################################################
# Docutils


def title_getter(node):
    """Return the title of a node (or "")."""
    for elem in node:
        if isinstance(elem, _TitleNode):
            return clean_astext(elem)
    return ""


class _StatementNode(nodes.General, nodes.Element):
    """Statement"""


class NumberedStatementNode(_StatementNode):
    """Statement with a number."""


class UnnumberedStatementNode(_StatementNode):
    """Statement without number.

    Some builders ignore this.
    """


class _TitleNode(nodes.TextElement):
    """Title of a statement"""


class _EmptyTitleNode(nodes.TextElement):
    """Dummy node for statements without any title."""


class ContentNode(nodes.General, nodes.Element):
    """Content of a proof or a statement"""


class StatementEnvironment(SphinxDirective):
    """A statement environment

    Copied from:
    https://github.com/sphinx-doc/sphinx/blob/6e8113da36c6db125dff78a38e086a29592c2867/sphinx/directives/patches.py#L109-L161
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self):
        """Render this environment"""
        env = self.state.document.settings.env

        thmtype = self.name[len("proof:") :]
        if thmtype in env.config.proof_html_nonumbers:
            node = UnnumberedStatementNode("\n".join(self.content))
        else:
            node = NumberedStatementNode("\n".join(self.content))
        node["thmtype"] = thmtype
        if self.arguments:
            titletext = self.arguments[0]
            titlenodes, messages = self.state.inline_text(titletext, self.lineno)
            title = _TitleNode(titletext, "", *titlenodes, **self.options)
            node += title
        else:
            title = _EmptyTitleNode("", "", **self.options)
            node += title
            messages = []

        content = ContentNode()
        self.state.nested_parse(self.content, self.content_offset, content)
        content["classes"] += ["proof-content"]
        node += content

        self.add_name(node)
        return [node] + messages


class ProofDomain(StandardDomain):
    """Proof domain"""

    name = "proof"
    label = "Proof"


################################################################################
# HTML


def get_fignumber(writer, node):
    """Compute and return the theorem number of `node`."""
    # Copied from the sphinx project: sphinx.writers.html.HTMLTranslator.add_fignumber()
    if not isinstance(node.parent, NumberedStatementNode):
        return ""
    figure_id = node.parent["ids"][0]
    if writer.builder.name == "singlehtml":
        key = f"{writer.docnames[-1]}/proof"
    else:
        key = "proof"
    if figure_id in writer.builder.fignumbers.get(key, {}):
        return ".".join(map(str, writer.builder.fignumbers[key][figure_id]))
    return ""


def html_visit_statement_node(self, node):
    """Enter :class:`_StatementNode` in HTML builder."""

    self.body.append(
        self.starttag(node, "div", CLASS=f"""proof proof-type-{node["thmtype"]}""")
    )


def html_depart_statement_node(self, node):
    """Leave :class:`_StatementNode` in HTML builder."""
    # pylint: disable=unused-argument
    self.body.append("</div>")


def html_visit_title_node(self, node):
    """Enter :class:`_TitleNode` in HTML builder."""

    config = self.builder.env.config
    thmtypes = config.proof_theorem_types
    thmtype = node.parent["thmtype"]

    self.body.append(
        jinja2.Template(self.builder.config.proof_html_title_template_visit).render(
            number=get_fignumber(self, node),
            thmtype=thmtypes[thmtype],
            title=isinstance(node, _TitleNode),
        )
    )


def html_depart_title_node(self, node):
    """Leave :class:`_TitleNode` in HTML builder."""

    config = self.builder.env.config
    thmtypes = config.proof_theorem_types
    thmtype = node.parent["thmtype"]

    self.body.append(
        jinja2.Template(self.builder.config.proof_html_title_template_depart).render(
            number=get_fignumber(self, node),
            thmtype=thmtypes[thmtype],
            title=isinstance(node, _TitleNode),
        )
    )


def html_visit_content_node(self, node):
    """Enter :class:`ContentNode` in HTML builder."""
    self.body.append(self.starttag(node, "div"))


def html_depart_content_node(self, node):
    """Leave :class:`ContentNode` in HTML builder."""
    # pylint: disable=unused-argument
    self.body.append("</div>")


################################################################################
# LaTeX


def latex_visit_statement_node(self, node):
    """Enter :class:`_StatementNode` in LaTeX builder."""
    self.body.append(rf"""\begin{{{node["thmtype"]}}}""")


def latex_visit_title_node(self, node):
    """Enter :class:`_TitleNode` in HTML builder."""
    if isinstance(node, _TitleNode):
        self.body.append("[")


def latex_depart_title_node(self, node):
    """Leave :class:`_TitleNode` in HTML builder."""
    if isinstance(node, _TitleNode):
        self.body.append("]")
    self.body.append(self.hypertarget_to(node.parent))
    self.body.append("\n")


def latex_depart_statement_node(self, node):
    """Leave :class:`_StatementNode` in LaTeX builder."""
    self.body.append(rf"""\end{{{node["thmtype"]}}}""")
    self.body.append("\n")


def latex_visit_content_node(self, node):  # pylint: disable=unused-argument
    """Enter :class:`ContentNode` in LaTeX builder."""


def latex_depart_content_node(self, node):  # pylint: disable=unused-argument
    """Leave :class:`ContentNode` in LaTeX builder."""


def _latex_preamble_iterator(config):
    thmtypes = config.proof_theorem_types

    yield r"\makeatletter"

    if not config.proof_latex_main in config.proof_latex_notheorem:
        if config.proof_latex_parent:
            newthm_format = r"\newtheorem{{{envname}}}{{{text}}}[{parent}]"
        else:
            newthm_format = r"\newtheorem{{{envname}}}{{{text}}}"
        yield newthm_format.format(
            envname=config.proof_latex_main,
            parent=config.proof_latex_parent,
            text=thmtypes[config.proof_latex_main],
        )

    for environment, thmtype in thmtypes.items():
        if not environment in config.proof_latex_notheorem + [config.proof_latex_main]:
            yield rf"\newtheorem{{{environment}}}[{config.proof_latex_main}]{{{thmtype}}}"

    yield r"\makeatother"


def latex_preamble(config):
    """Return the custom LaTeX preamble."""
    return "\n".join(_latex_preamble_iterator(config))


################################################################################
# Setup


def process_proof_theorem_types(app, config):
    """Hook called when builder has been inited."""
    # Create directives
    for environment in config.proof_theorem_types:
        app.add_directive_to_domain("proof", environment, StatementEnvironment)

    # Generate LaTeX preamble
    if "preamble" not in config.latex_elements:
        config.latex_elements["preamble"] = ""
    config.latex_elements["preamble"] += latex_preamble(config)


def init_numfig_format(app, config):
    """Initialize :confval:`numfig_format`."""
    # pylint: disable=unused-argument
    numfig_format = {"proof": "Proof %s"}

    # override default labels by configuration
    numfig_format.update(config.numfig_format)
    config.numfig_format = numfig_format


def setup(app):
    """Plugin setup"""

    app.add_domain(ProofDomain)

    app.add_css_file("proof.css")
    app.add_js_file("proof.js")

    app.add_config_value(
        "proof_html_title_template_visit", PROOF_HTML_TITLE_TEMPLATE_VISIT, "env"
    )
    app.add_config_value(
        "proof_html_title_template_depart", PROOF_HTML_TITLE_TEMPLATE_DEPART, "env"
    )
    app.add_config_value("proof_html_nonumbers", PROOF_HTML_NONUMBERS, "env")
    app.add_config_value("proof_latex_main", "theorem", "env")
    app.add_config_value("proof_latex_notheorem", [], "env")
    app.add_config_value("proof_latex_parent", None, "env")
    app.add_config_value("proof_theorem_types", PROOF_THEOREM_TYPES, "env")

    app.add_enumerable_node(
        NumberedStatementNode,
        "proof",
        title_getter,
        html=(html_visit_statement_node, html_depart_statement_node),
        singlehtml=(html_visit_statement_node, html_depart_statement_node),
        latex=(latex_visit_statement_node, latex_depart_statement_node),
    )
    app.add_node(
        UnnumberedStatementNode,
        html=(html_visit_statement_node, html_depart_statement_node),
        singlehtml=(html_visit_statement_node, html_depart_statement_node),
        latex=(latex_visit_statement_node, latex_depart_statement_node),
    )
    app.add_node(
        ContentNode,
        html=(html_visit_content_node, html_depart_content_node),
        singlehtml=(html_visit_content_node, html_depart_content_node),
        latex=(latex_visit_content_node, latex_depart_content_node),
    )
    app.add_node(
        _TitleNode,
        html=(html_visit_title_node, html_depart_title_node),
        singlehtml=(html_visit_title_node, html_depart_title_node),
        latex=(latex_visit_title_node, latex_depart_title_node),
    )
    app.add_node(
        _EmptyTitleNode,
        html=(html_visit_title_node, html_depart_title_node),
        singlehtml=(html_visit_title_node, html_depart_title_node),
        latex=(latex_visit_title_node, latex_depart_title_node),
    )

    app.connect("config-inited", process_proof_theorem_types)
    app.connect("config-inited", init_numfig_format)
