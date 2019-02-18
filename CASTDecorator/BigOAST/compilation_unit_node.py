import json

from pycparser.c_ast import FileAST

from BigOAST.basic_node import BasicNode


class CompilationUnitNode(BasicNode):
    def __init__(self, node: FileAST):
        super().__init__(node)

        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
