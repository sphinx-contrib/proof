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

from sphinx.domains import Domain
from sphinx.roles import XRefRole
from sphinx.util import copy_static_entry
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info, make_refnode

VERSION = "1.0.1"
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

PROOF_UNNUMBERED_TYPES = ["proof"]

HTML_PROOF_TITLE_TEMPLATE = u"""
<div class="proof-title">
    <span class="proof-type">{{ thmtype }} {% if number %}{{number}}{% endif %}</span>
    {% if title %}
    <span class="proof-title-name">({{ title }})</span>
    {% endif %}
</div>
"""

################################################################################
# Docutils


class StatementNode(nodes.General, nodes.Element):
    """Statement"""

    pass


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
    option_spec = {"label": directives.unchanged_required}

    def run(self):
        """Render this environment"""
        env = self.state.document.settings.env
        # targetid = "index-%s" % env.new_serialno("index")
        # targetnode = nodes.target("", "", ids=[targetid])

        node = StatementNode("\n".join(self.content))
        node["thmtype"] = self.name[len(PREFIX) :]
        if "label" in self.options:
            node["label"] = self.options.get("label")
        else:
            node["label"] = ""
        node["classes"] += ["proof", "proof-type-{}".format(node["thmtype"])]
        if self.arguments:
            node["title"] = self.arguments[0]

        content = ContentNode()
        self.state.nested_parse(self.content, self.content_offset, content)
        content["classes"] += ["proof-content"]
        node += content

        ret = [node]
        set_source_info(self, node)
        if node["thmtype"] not in env.config.proof_unnumbered_types:
            self.add_target(ret)
        return ret

    def add_target(self, ret):
        # type: (List[nodes.Node]) -> None
        #
        # pylint: disable=missing-docstring
        # This is bad, but this was copy-pasted and I do not understand it. Shame on me.
        node = ret[0]

        # assign label automatically if no label defined
        if not node["label"]:
            seq = self.env.new_serialno("sphinxcontrib.proof#theorems")
            node["label"] = "%s:%d" % (self.env.docname, seq)

        # no targets and numbers are needed
        if not node["label"]:
            return

        # register label to domain
        domain = self.env.get_domain("proof")
        try:
            thno = domain.add_theorem(
                self.env, self.env.docname, node["label"], node["thmtype"]
            )  # type: ignore  # NOQA
            node["number"] = thno

            # add target node
            node_id = make_id("proof-%s" % node["label"])
            target = nodes.target("", "", ids=[node_id])
            self.state.document.note_explicit_target(target)
            ret.insert(0, target)
        except UserWarning as exc:
            self.state_machine.reporter.warning(exc.args[0], line=self.lineno)


class TheoremReferenceRole(XRefRole):
    # pylint: disable=missing-docstring
    # This is bad, but this was copy-pasted and I do not understand it. Shame on me.

    def result_nodes(self, document, env, node, is_ref):
        # type: (nodes.Node, BuildEnvironment, nodes.Node, bool) -> Tuple[List[nodes.Node], List[nodes.Node]]  # pylint: disable=line-too-long
        node["refdomain"] = "proof"
        return [node], []

    def process_link(self, env, refnode, has_explicit_title, title, target):
        # pylint: disable=too-many-arguments
        # type: (BuildEnvironment, nodes.reference, bool, unicode, unicode) -> Tuple[unicode, unicode]  # pylint: disable=line-too-long
        if has_explicit_title:
            refnode["title"] = title
        return super().process_link(env, refnode, has_explicit_title, title, target)


class ProofDomain(Domain):
    """Proof domain

    Copied from:
    https://github.com/sphinx-doc/sphinx/blob/836fe2f3a9bd4d1fd4187f9ecf6e2976156dbfd3/sphinx/domains/math.py#L40-L123

    :copyright: Copyright 2007-2018 by the Sphinx team. Some edits by Louis Paternault.
    """

    name = "proof"
    label = "proof"

    initial_data = {
        "objects": {}  # labelid -> (docname, thno, thmtype)
    }  # type: Dict[unicode, Dict[unicode, Tuple[unicode, int]]]
    roles = {"thm": TheoremReferenceRole()}

    def clear_doc(self, docname):
        # pylint: disable=unused-variable
        # type: (unicode) -> None
        for theorem_id, (doc, thno, thmtype) in list(self.data["objects"].items()):
            if doc == docname:
                del self.data["objects"][theorem_id]

    def merge_domaindata(self, docnames, otherdata):
        # type: (Iterable[unicode], Dict) -> None
        for labelid, (doc, thno, thmtype) in otherdata["objects"].items():
            if doc in docnames:
                self.data["objects"][labelid] = (doc, thno, thmtype)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        # pylint: disable=too-many-arguments, too-many-locals
        # type: (BuildEnvironment, unicode, Builder, unicode, unicode, nodes.Node, nodes.Node) -> nodes.Node  # pylint: disable=line-too-long
        assert typ == "thm"
        docname, number, thmtype = self.data["objects"].get(target, (None, None, None))
        if docname:
            node_id = make_id("proof-%s" % target)
            if "title" in node:
                title = nodes.Text(node["title"])
            else:
                try:
                    thm_format = env.config.proof_ref_format or "({number})"
                    title = nodes.Text(
                        thm_format.format(
                            number=number,
                            thmtype=env.config.proof_theorem_types[thmtype],
                        )
                    )
                except KeyError as exc:
                    logging.warning("Invalid proof_ref_format: %r", exc, location=node)
                    title = nodes.Text("(%d)" % number)
            return make_refnode(builder, fromdocname, docname, node_id, title)
        else:
            return None

    def resolve_any_xref(self, env, fromdocname, builder, target, node, contnode):
        # pylint: disable=too-many-arguments, no-else-return
        # type: (BuildEnvironment, unicode, Builder, unicode, nodes.Node, nodes.Node) -> List[nodes.Node]  # pylint: disable=line-too-long
        refnode = self.resolve_xref(
            env, fromdocname, builder, "thm", target, node, contnode
        )
        if refnode is None:
            return []
        else:
            return [refnode]

    def get_objects(self):
        # type: () -> List
        return []

    def add_theorem(self, env, docname, labelid, thmtype):
        # type: (BuildEnvironment, unicode, unicode, unicode) -> int
        #
        # pylint: disable=missing-docstring
        # This is bad, but this was copy-pasted and I do not understand it. Shame on me.
        theorems = self.data["objects"]
        if labelid in theorems:
            path = env.doc2path(theorems[labelid][0])
            msg = "duplicate label of theorem %s, other instance in %s" % (
                labelid,
                path,
            )
            raise UserWarning(msg)
        else:
            thno = self.get_next_theorem_number(docname)
            theorems[labelid] = (docname, thno, thmtype)
            return thno

    def get_next_theorem_number(self, docname):
        # pylint: disable=unused-argument
        # type: (unicode) -> int
        """Return the next available theorem number."""
        targets = [eq for eq in self.data["objects"].values()]

        # Uncomment to have per-chapter theorem numbers (i.e.
        # numbers start back to zero on each new chapter)
        # targets = [eq for eq in self.data["objects"].values() if eq[0] == docname]

        return len(targets) + 1


################################################################################
# HTML
def html_visit_statement_node(self, node):
    """Enter :class:`StatementNode` in HTML builder."""
    thmtypes = self.builder.config.proof_theorem_types
    if self.builder.config.html_proof_number_theorems:
        number = node.get("number", None)
    else:
        number = None
    self.body.append(self.starttag(node, "div"))
    self.body.append(
        self.builder.config.html_proof_title_template_compiled.render(
            number=number,
            thmtype=thmtypes[node["thmtype"]],
            title=node.get("title", None),
        )
    )


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
    self.body.append(r"\begin{{{}}}".format(node["thmtype"]))
    if "title" in node:
        self.body.append("[{}]".format(node["title"]))
    self.body.append("\n")


def latex_depart_statement_node(self, node):
    """Leave :class:`StatementNode` in LaTeX builder."""
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

    if not config.latex_proof_main in config.latex_proof_notheorem:
        if config.latex_proof_parent:
            newthm_format = r"\newtheorem{{{envname}}}{{{text}}}[{parent}]"
        else:
            newthm_format = r"\newtheorem{{{envname}}}{{{text}}}"
        yield newthm_format.format(
            envname=config.latex_proof_main,
            parent=config.latex_proof_parent,
            text=thmtypes[config.latex_proof_main],
        )

    for environment, thmtype in thmtypes.items():
        if not environment in config.latex_proof_notheorem + [config.latex_proof_main]:
            yield r"\newtheorem{%s}[%s]{%s}" % (
                environment,
                config.latex_proof_main,
                thmtype,
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
    if app.builder.name == "html":
        config.html_proof_title_template_compiled = jinja2.Template(
            config.html_proof_title_template
        )


def setup(app):
    """Plugin setup"""

    app.add_domain(ProofDomain)

    app.add_stylesheet("proof.css")
    app.add_javascript("proof.js")

    app.add_config_value("html_proof_number_theorems", True, "env")
    app.add_config_value("html_proof_title_template", HTML_PROOF_TITLE_TEMPLATE, "env")
    app.add_config_value("latex_proof_main", "theorem", "env")
    app.add_config_value("latex_proof_parent", None, "env")
    app.add_config_value("latex_proof_notheorem", [], "env")
    app.add_config_value("proof_ref_format", "{thmtype} {number}", "env")
    app.add_config_value("proof_theorem_types", PROOF_THEOREM_TYPES, "env")
    app.add_config_value("proof_unnumbered_types", PROOF_UNNUMBERED_TYPES, "env")

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

    app.add_role("thm", TheoremReferenceRole(warn_dangling=True))

    for environment in app.config.proof_theorem_types:
        app.add_directive(PREFIX + environment, StatementEnvironment)

    app.connect("builder-inited", builder_inited)
