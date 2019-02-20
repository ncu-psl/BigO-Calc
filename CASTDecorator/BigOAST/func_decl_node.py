from pycparser.c_ast import FuncDef

from BigOAST.basic_node import BasicNode
from BigOAST.func_call_node import FuncCallNode


class FuncDeclNode(BasicNode):
    def __init__(self, func_decl: FuncDef):
        super().__init__(func_decl)

        self.recursive = False
        self.name = func_decl.decl.name

        self.parameter = []
        if func_decl.decl.type.args:
            param_list = func_decl.decl.type.args.params
            for param in param_list:
                self.parameter.append(param.type.type.names[0] + ' ' + param.name)

        pass

    def check_recursion(self):
        que = [self]

        while que:
            node = que.pop(0)
            if isinstance(node, FuncCallNode):
                if node.name == self.name:
                    self.recursive = True
                    break
            for child in node.children:
                que.append(child)

        pass
    def to_dect(self):
        d = super().to_dect()
        d.update({'recursive': self.recursive})
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d
