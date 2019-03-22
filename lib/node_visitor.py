"""
    :copyright: Copyright 2008 by Armin Ronacher.
    :license: Python License.
    :modified by dongying he
"""
from collections import Iterable


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if node and hasattr(node, 'children'):
            for value in node.children:
                if isinstance(value, list):
                    for item in value:
                        self.visit(item)
                else:
                    self.visit(value)
