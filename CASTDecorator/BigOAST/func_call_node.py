from pycparser.c_ast import FuncCall, Constant, ID

from BigOAST.basic_node import BasicNode


class FuncCallNode(BasicNode):
    def __init__(self, func_call: FuncCall = None):
        super().__init__(func_call)

        self.name = ''
        self.parameter = []

        if func_call is None:
            return

        self.name = func_call.name.name
        if func_call.args:
            for param in func_call.args.exprs:
                if isinstance(param, Constant):
                    self.parameter.append(param.value)
                elif isinstance(param, ID):
                    self.parameter.append(param.name)

        pass

    def to_dect(self):
        d = super().to_dect()
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d
