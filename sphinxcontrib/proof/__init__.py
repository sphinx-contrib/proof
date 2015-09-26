# -*- coding: utf-8 -*-

# Copyright 2015 Louis Paternault
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
import pkg_resources

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.util import copy_static_entry
from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive

def package_file(*filename):
    """Return the path to a filename present in package data."""
    return pkg_resources.resource_filename("sphinxcontrib.proof", os.path.join("data", *filename))

VERSION = "0.1.0"
PREFIX = "proof:"

class StatementNode(nodes.General, nodes.Element):
    """Statement"""
    pass
class ProofNode(nodes.Part, nodes.Element):
    """Proof"""
    pass
class ContentNode(nodes.General, nodes.Element):
    """Content of a proof or a statement"""
    pass

# This should be internationalized using gettext… Patch welcome!
FRENCH = {
    'lemma': u"Lemme",
    'property': u"Propriété",
    'example': u"Exemple",
    'theorem': u"Théorème",
    'definition': u"Définition",
    'proof': u"Preuve",
    'conjecture': u"Conjecture",
    'algorithm': u"Algorithme",
    }


class ProofEnvironment(Directive):
    """A proof environment"""

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'label': directives.unchanged_required,
        }

    def run(self):
        """Render this environment"""
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])

        node = ProofNode('\n'.join(self.content))
        node['classes'] += ['proof-type-proof']

        if self.arguments:
            node['title'] = self.arguments[0]

        content = ContentNode()
        self.state.nested_parse(self.content, self.content_offset, content)
        content['classes'] += ['proof-content']
        node += content

        set_source_info(self, node)
        return [targetnode, node]

class StatementEnvironment(Directive):
    """A statement environment"""

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'label': directives.unchanged_required,
        }

    def run(self):
        """Render this environment"""
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])

        node = StatementNode('\n'.join(self.content))
        node['name'] = self.name[len(PREFIX):]
        node['classes'] += ['proof', 'proof-type-{}'.format(node['name'])]
        if self.arguments:
            node['title'] = self.arguments[0]

        content = ContentNode()
        self.state.nested_parse(self.content, self.content_offset, content)
        content['classes'] += ['proof-content']
        node += content

        set_source_info(self, node)
        return [targetnode, node]

# HTML
def html_visit_proof_node(self, node):
    """Enter :class:`ProofNode` in HTML builder."""
    self.body.append(self.starttag(node, 'div'))
    self.body.append("""<div class="proof-title">""")
    self.body.append("""<span class="proof-title-name">Preuve</span>""")
    if 'title' in node:
        self.body.append("""<span class="proof-title-content">""")
        self.body.append(u"({})".format(node['title']))
        self.body.append("""</span>""")
    self.body.append("""</div>""")

def html_depart_proof_node(self, node):
    """Leave :class:`ProofNode` in HTML builder."""
    # pylint: disable=unused-argument
    self.body.append('</div>')


def html_visit_statement_node(self, node):
    """Enter :class:`StatementNode` in HTML builder."""
    self.body.append(self.starttag(node, 'div'))
    self.body.append("""<div class="proof-title">""")
    self.body.append(u"""<span class="proof-title-name">{}</span>""".format(FRENCH[node['name']]))
    if 'title' in node:
        self.body.append("""<span class="proof-title-content">""")
        self.body.append(u"({})".format(node['title']))
        self.body.append("""</span>""")
    self.body.append("""</div>""")

def html_depart_statement_node(self, node):
    """Leave :class:`StatementNode` in HTML builder."""
    # pylint: disable=unused-argument
    self.body.append('</div>')


def html_visit_content_node(self, node):
    """Enter :class:`ContentNode` in HTML builder."""
    self.body.append(self.starttag(node, 'div'))

def html_depart_content_node(self, node):
    """Leave :class:`ContentNode` in HTML builder."""
    # pylint: disable=unused-argument
    self.body.append('</div>')

# LaTeX
def latex_visit_proof_node(self, node):
    """Enter :class:`ProofNode` in LaTeX builder."""
    self.body.append(r"\begin{proof}")
    if 'title' in node:
        self.body.append("[{}]".format(node['title']))
    self.body.append("\n")

def latex_depart_proof_node(self, node):
    """Leave :class:`ProofNode` in LaTeX builder."""
    # pylint: disable=unused-argument
    self.body.append(r"\end{proof}")
    self.body.append("\n")


def latex_visit_statement_node(self, node):
    """Enter :class:`StatementNode` in LaTeX builder."""
    self.body.append(r"\begin{{{}}}".format(node['name']))
    if 'title' in node:
        self.body.append("[{}]".format(node['title']))
    self.body.append("\n")

def latex_depart_statement_node(self, node):
    """Leave :class:`StatementNode` in LaTeX builder."""
    self.body.append(r"\end{{{}}}".format(node['name']))
    self.body.append("\n")


def latex_visit_content_node(self, node):
    """Enter :class:`ContentNode` in LaTeX builder."""
    # pylint: disable=unused-argument
    pass

def latex_depart_content_node(self, node):
    """Leave :class:`ContentNode` in LaTeX builder."""
    # pylint: disable=unused-argument
    pass

def builder_inited(app):
    """Hook called when builder has been inited."""
    if app.builder.name == "latex":
        app.builder.config.latex_additional_files.append(
            package_file("_static", "sphinxcontribproof.sty")
            )

def setup(app):
    """Plugin setup"""
    app.add_stylesheet("proof.css")
    app.add_javascript("proof.js")

    app.add_node(
        ProofNode,
        html=(html_visit_proof_node, html_depart_proof_node),
        latex=(latex_visit_proof_node, latex_depart_proof_node),
        )
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

    app.add_directive(PREFIX + 'property', StatementEnvironment)
    app.add_directive(PREFIX + 'lemma', StatementEnvironment)
    app.add_directive(PREFIX + 'example', StatementEnvironment)
    app.add_directive(PREFIX + 'theorem', StatementEnvironment)
    app.add_directive(PREFIX + 'definition', StatementEnvironment)
    app.add_directive(PREFIX + 'proof', ProofEnvironment)
    app.add_directive(PREFIX + 'conjecture', StatementEnvironment)
    app.add_directive(PREFIX + 'algorithm', StatementEnvironment)

    app.connect('builder-inited', builder_inited)
    app.add_latex_package("sphinxcontribproof")
