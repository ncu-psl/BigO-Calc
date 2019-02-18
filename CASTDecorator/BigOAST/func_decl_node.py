import json

from pycparser.c_ast import FuncDef

from BigOAST.basic_node import BasicNode


class FuncDeclNode(BasicNode):
    def __init__(self, func_decl: FuncDef):
        super().__init__(func_decl)

        self.name = func_decl.decl.name
        self.is_recursive_func = False
        self.parameter = []
        if func_decl.decl.type.args:
            param_list = func_decl.decl.type.args.params
            for param in param_list:
                self.parameter.append(param.type.type.names[0] + ' ' + param.name)

        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
