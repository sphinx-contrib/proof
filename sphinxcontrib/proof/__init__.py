# Copyright 2018 Louis Paternault
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

from sphinx.domains.std import StandardDomain
from sphinx.domains import ObjType
from sphinx.roles import XRefRole
from sphinx.util import copy_static_entry
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info, make_refnode

VERSION = "1.1.0"
PREFIX = "proof:"

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

PROOF_HTML_TITLE_TEMPLATE = u"""
    <div class="proof-title">
        <span class="proof-type">{{ thmtype }} {% if number %}{{number}}{% endif %}</span>
        {% if title %}
            <span class="proof-title-name">({{ title }})</span>
        {% endif %}
    </div>
"""


################################################################################
# Docutils


def title_getter(node):
    """Return the title of a node (or `None`)."""
    if "title" in node:
        return node["title"]
    return ""


class _StatementNode(nodes.General, nodes.Element):
    """Statement"""

    pass


class NumberedStatementNode(_StatementNode):
    """Statement with a number."""

    numbered = True


class UnnumberedStatementNode(_StatementNode):
    """Statement without number.

    Some builders ignore this.
    """

    numbered = False


class ContentNode(nodes.General, nodes.Element):
    """Content of a proof or a statement"""

    pass


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

        thmtype = self.name[len(PREFIX) :]
        if thmtype in env.config.proof_html_nonumbers:
            node = UnnumberedStatementNode("\n".join(self.content))
        else:
            node = NumberedStatementNode("\n".join(self.content))
        node["thmtype"] = thmtype
        if self.arguments:
            node["title"] = self.arguments[0]

        content = ContentNode()
        self.state.nested_parse(self.content, self.content_offset, content)
        content["classes"] += ["proof-content"]
        node += content

        self.add_name(node)
        return [node]


class ProofDomain(StandardDomain):
    """Proof domain"""

    name = "proof"
    label = "proof"


################################################################################
# HTML
def html_visit_statement_node(self, node):
    """Enter :class:`_StatementNode` in HTML builder."""

    def get_fignumber():
        # Copied from the sphinx project: sphinx.writers.html.HTMLTranslator.add_fignumber()
        if not isinstance(node, NumberedStatementNode):
            return ""
        figure_id = node["ids"][0]
        if self.builder.name == "singlehtml":
            key = u"%s/%s" % (self.docnames[-1], "proof")
        else:
            key = "proof"
        if figure_id in self.builder.fignumbers.get(key, {}):
            return ".".join(map(str, self.builder.fignumbers[key][figure_id]))
        return ""

    config = self.builder.env.config
    thmtypes = config.proof_theorem_types
    thmtype = node["thmtype"]

    self.body.append(
        self.starttag(node, "div", CLASS="proof proof-type-{}".format(thmtype))
    )
    self.body.append(
        jinja2.Template(self.builder.config.proof_html_title_template).render(
            number=get_fignumber(),
            thmtype=thmtypes[node["thmtype"]],
            title=node.get("title", None),
        )
    )


def html_depart_statement_node(self, node):
    """Leave :class:`_StatementNode` in HTML builder."""
    # pylint: disable=unused-argument
    self.body.append("</div>")


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
    self.body.append(r"\begin{{{}}}".format(node["thmtype"]))
    if "title" in node:
        self.body.append("[{}]".format(node["title"]))
    self.body.append(self.hypertarget_to(node))
    self.body.append("\n")


def latex_depart_statement_node(self, node):
    """Leave :class:`_StatementNode` in LaTeX builder."""
    self.body.append(r"\end{{{}}}".format(node["thmtype"]))
    self.body.append("\n")


def latex_visit_content_node(self, node):
    """Enter :class:`ContentNode` in LaTeX builder."""
    # pylint: disable=unused-argument
    pass


def latex_depart_content_node(self, node):
    """Leave :class:`ContentNode` in LaTeX builder."""
    # pylint: disable=unused-argument
    pass


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
            yield r"\newtheorem{%s}[%s]{%s}" % (
                environment,
                config.proof_latex_main,
                thmtype,
            )

    yield r"\makeatother"


def latex_preamble(config):
    """Return the custom LaTeX preamble."""
    return "\n".join(_latex_preamble_iterator(config))


################################################################################
# Setup


def generate_latex_preamble(app):
    """Hook called when builder has been inited."""
    config = app.builder.config
    if app.builder.name == "latex":
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

    app.add_stylesheet("proof.css")
    app.add_javascript("proof.js")

    app.add_config_value("proof_html_title_template", PROOF_HTML_TITLE_TEMPLATE, "env")
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

    for environment in app.config.proof_theorem_types:
        app.add_directive(PREFIX + environment, StatementEnvironment)

    app.connect("builder-inited", generate_latex_preamble)
    app.connect("config-inited", init_numfig_format)
