import json

from pycparser.c_ast import FuncCall, Constant, ID

from BigOAST.basic_node import BasicNode


class FuncCallNode(BasicNode):
    def __init__(self, func_call: FuncCall):
        super().__init__(func_call)

        self.name = func_call.name.name

        self.parameter = []
        if func_call.args:
            for param in func_call.args.exprs:
                if isinstance(param, Constant):
                    self.parameter.append(param.value)
                elif isinstance(param, ID):
                    self.parameter.append(param.name)

        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
