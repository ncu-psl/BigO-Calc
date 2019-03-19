from bigo_ast.bigo_ast import BasicNode
from lib.node_visitor import NodeVisitor


class BigOAstVisitor(NodeVisitor):
    root = BasicNode()
