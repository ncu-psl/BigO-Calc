import json

from pycparser.c_ast import FuncCall

from BigOAST.basic_node import BasicNode


class FuncCallNode(BasicNode):
    def __init__(self, func_call: FuncCall):
        super().__init__(func_call)

        self.name = func_call.name.name

        self.parameter = ' '.join(str(x) for x in func_call.args or [])
        self.is_recursive_call = False

        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
