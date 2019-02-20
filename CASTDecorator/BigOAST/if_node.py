from pycparser.c_ast import If

from BigOAST.basic_node import BasicNode


class IfNode(BasicNode):
    def __init__(self, if_node: If = None):
        super().__init__(if_node)

        self.condition = ''

        if if_node is None:
            return

        self.condition = ' '.join(str(x) for x in if_node.cond or [])

        pass

    def to_dect(self):
        d = super().to_dect()
        d.update({'condition': self.condition})

        return d
