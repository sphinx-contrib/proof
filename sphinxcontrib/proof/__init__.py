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

import os
from docutils import nodes
from docutils.parsers.rst import directives, Directive

from sphinx.util import copy_static_entry
from sphinx.util.nodes import set_source_info

VERSION = "1.0.1"
PREFIX = "proof:"

################################################################################
# Configuration
PROOF_THEOREM_LABELS = {
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

################################################################################
# Docutils


class StatementNode(nodes.General, nodes.Element):
    """Statement"""

    pass


class ContentNode(nodes.General, nodes.Element):
    """Content of a proof or a statement"""

    pass


class StatementEnvironment(Directive):
    """A statement environment"""

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {"label": directives.unchanged_required}

    def run(self):
        """Render this environment"""
        env = self.state.document.settings.env
        targetid = "index-%s" % env.new_serialno("index")
        targetnode = nodes.target("", "", ids=[targetid])

        node = StatementNode("\n".join(self.content))
        node["name"] = self.name[len(PREFIX) :]
        node["classes"] += ["proof", "proof-type-{}".format(node["name"])]
        if self.arguments:
            node["title"] = self.arguments[0]

        content = ContentNode()
        self.state.nested_parse(self.content, self.content_offset, content)
        content["classes"] += ["proof-content"]
        node += content

        set_source_info(self, node)
        return [targetnode, node]


################################################################################
# HTML
def html_visit_statement_node(self, node):
    """Enter :class:`StatementNode` in HTML builder."""
    labels = self.builder.config.proof_theorem_labels
    self.body.append(self.starttag(node, "div"))
    self.body.append("""<div class="proof-title">""")
    self.body.append(
        u"""<span class="proof-title-name">{}</span>""".format(
            labels.get(node["name"], "unknown-theorem-type")
        )
    )
    if "title" in node:
        self.body.append("""<span class="proof-title-content">""")
        self.body.append(u"({})".format(node["title"]))
        self.body.append("""</span>""")
    self.body.append("""</div>""")


def html_depart_statement_node(self, node):
    """Leave :class:`StatementNode` in HTML builder."""
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
    """Enter :class:`StatementNode` in LaTeX builder."""
    self.body.append(r"\begin{{{}}}".format(node["name"]))
    if "title" in node:
        self.body.append("[{}]".format(node["title"]))
    self.body.append("\n")


def latex_depart_statement_node(self, node):
    """Leave :class:`StatementNode` in LaTeX builder."""
    self.body.append(r"\end{{{}}}".format(node["name"]))
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
    labels = config.proof_theorem_labels

    yield config.latex_elements.get("preamble", "")

    yield r"\makeatletter"

    if config.latex_proof_counter:
        yield r"\newtheorem{%s}{%s}[%s]" % (
            config.latex_proof_main,
            labels[config.latex_proof_main],
            config.latex_proof_counter,
        )
    else:
        yield r"\newtheorem{%s}{%s}" % (
            config.latex_proof_main,
            labels[config.latex_proof_main],
        )

    for environment, label in labels.items():
        if not environment in config.latex_proof_notheorem + [config.latex_proof_main]:
            yield r"\newtheorem{%s}[%s]{%s}" % (
                environment,
                config.latex_proof_main,
                label,
            )

    yield r"\makeatother"


def latex_preamble(config):
    """Return the custom LaTeX preamble."""
    return "\n".join(_latex_preamble_iterator(config))


################################################################################
# Setup


def builder_inited(app):
    """Hook called when builder has been inited."""
    config = app.builder.config
    if app.builder.name == "latex":
        if "preamble" not in config.latex_elements:
            config.latex_elements["preamble"] = ""
        config.latex_elements["preamble"] += latex_preamble(config)


def setup(app):
    """Plugin setup"""
    app.add_stylesheet("proof.css")
    app.add_javascript("proof.js")

    app.add_config_value("proof_theorem_labels", PROOF_THEOREM_LABELS, "env")
    app.add_config_value("latex_proof_counter", "", "env")
    app.add_config_value("latex_proof_main", "theorem", "env")
    app.add_config_value("latex_proof_notheorem", [], "env")

    app.add_node(
        StatementNode,
        html=(html_visit_statement_node, html_depart_statement_node),
        latex=(latex_visit_statement_node, latex_depart_statement_node),
    )
    app.add_node(
        ContentNode,
        html=(html_visit_content_node, html_depart_content_node),
        latex=(latex_visit_content_node, latex_depart_content_node),
    )

    for environment in app.config.proof_theorem_labels:
        app.add_directive(PREFIX + environment, StatementEnvironment)

    app.connect("builder-inited", builder_inited)
