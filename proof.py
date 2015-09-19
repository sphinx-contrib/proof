#!/usr/bin/env python3

# Copyright 2014-2015 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""TODO Update comments and documentation"""

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.locale import _
from sphinx.environment import NoUri
from sphinx.util.nodes import set_source_info
from sphinx.util.compat import Directive, make_admonition

PREFIX = "proof:"

class StatementNode(nodes.General, nodes.Element): pass
class ProofNode(nodes.Part, nodes.Element): pass
class ContentNode(nodes.General, nodes.Element): pass

HUMAN = {
        'lemma': "Lemme",
        'property': "Propriété",
        'example': "Exemple",
        'theorem': "Théorème",
        'definition': "Définition",
        'proof': "Preuve",
        'conjecture': "Conjecture",
        'algorithm': "Algorithme",
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
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])

        node = ProofNode('\n'.join(self.content))
        node['classes'] += ['proof-type-proof']

        if self.arguments:
            node['title'] = self.arguments[0]
        else:
            node['title'] = None

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
    self.body.append(self.starttag(node, 'div'))
    self.body.append("""<div class="proof-title">""")
    self.body.append("""<span class="proof-title-name">Preuve</span>""")
    if 'title' in node:
        self.body.append(""" <span class="proof-title-content">({})</span>""".format(node['title']))
    self.body.append("""</div>""")
def html_depart_proof_node(self, node):
    self.body.append('</div>')

def html_visit_statement_node(self, node):
    self.body.append(self.starttag(node, 'div'))
    self.body.append("""<div class="proof-title">""")
    self.body.append("""<span class="proof-title-name">{}</span>""".format(HUMAN[node['name']]))
    if 'title' in node:
        self.body.append(""" <span class="proof-title-content">({})</span>""".format(node['title']))
    self.body.append("""</div>""")
def html_depart_statement_node(self, node):
    self.body.append('</div>')

def html_visit_content_node(self, node):
    self.body.append(self.starttag(node, 'div'))
def html_depart_content_node(self, node):
    self.body.append('</div>')

# LaTeX
def latex_visit_proof_node(self, node):
    self.body.append("DEBUT proof")
def latex_depart_proof_node(self, node):
    self.body.append('FIN proof')

def latex_visit_statement_node(self, node):
    self.body.append("DEBUT statement")
def latex_depart_statement_node(self, node):
    self.body.append('FIN statement')

def latex_visit_content_node(self, node):
    self.body.append("DEBUT content")
def latex_depart_content_node(self, node):
    self.body.append('FIN content')

# Setup
def setup(app):
    app.add_javascript('proof.js')
    app.add_stylesheet('proof.css')

    app.add_node(ProofNode,
                 html=(html_visit_proof_node, html_depart_proof_node),
                 latex=(latex_visit_proof_node, latex_depart_proof_node),
                 )
    app.add_node(StatementNode,
                 html=(html_visit_statement_node, html_depart_statement_node),
                 latex=(latex_visit_statement_node, latex_depart_statement_node),
                 )
    app.add_node(ContentNode,
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

