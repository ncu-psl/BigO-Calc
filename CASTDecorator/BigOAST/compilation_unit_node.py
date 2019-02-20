from pycparser.c_ast import FileAST

from BigOAST.basic_node import BasicNode


class CompilationUnitNode(BasicNode):
    def __init__(self, node: FileAST = None):
        super().__init__(node)

        if node is None:
            return

        pass
