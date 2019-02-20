from pycparser.c_ast import If

from BigOAST.basic_node import BasicNode


class IfNode(BasicNode):
    def __init__(self, if_node: If):
        super().__init__(if_node)

        self.condtion = ' '.join(str(x) for x in if_node.cond or [])

        pass

    def to_dect(self):
        d = super().to_dect()
        d.update({'condtion': self.condtion})

        return d
