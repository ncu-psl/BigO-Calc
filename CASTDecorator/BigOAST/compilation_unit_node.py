from pycparser.c_ast import FileAST

from BigOAST.basic_node import BasicNode


class CompilationUnitNode(BasicNode):
    def __init__(self, node: FileAST):
        super().__init__(node)

        pass
