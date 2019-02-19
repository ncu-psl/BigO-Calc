import json

from pycparser.c_ast import Node


class BasicNode(object):
    def __init__(self, node: Node = None):
        self.time_complexity = ''
        self.children = []
        self.col = 0
        self.line_number = 0
        self.parent = None
        self._type = self.__class__.__name__

        if node is None:
            return

        if not issubclass(node.__class__, Node) or node is Node:
            raise Exception("Should init with a subclass of pycparser.c_ast.Node")

        if node.coord:
            self.col = node.coord.column
            self.line_number = node.coord.line

        pass

    def toJSON(self):
        self.parent = None
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
