from BigOAST.basic_node import BasicNode
from BigOAST.func_call_node import FuncCallNode


class FuncDeclNode(BasicNode):
    #__slots__ = ["time_complexity", "children", "col", "line_number", "parent", "_type", "recursive", "name", "parameter"]

    def __init__(self, basic: BasicNode):
        super().__init__()

        self.recursive = False
        self.name = ''
        self.parameter = []

        pass

    def determine_recursion(self):
        que = [self]

        while que:
            node = que.pop(0)
            if isinstance(node, FuncCallNode):
                if node.name == self.name:
                    self.recursive = True
                    break
            for child in node.children:
                que.append(child)

        return self.recursive

    def to_dect(self):
        d = super().to_dect()
        d.update({'recursive': self.recursive})
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d
