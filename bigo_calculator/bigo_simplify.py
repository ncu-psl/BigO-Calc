import sympy

from bigo_ast.bigo_ast import BasicNode, FuncDeclNode
from bigo_ast.bigo_ast_visitor import BigOAstVisitor


class BigOSimplify(BigOAstVisitor):
    def __init__(self, root: BasicNode):
        self.root = root
        self.func_list = []
        for func in self.root.children:
            if type(func) == FuncDeclNode:
                self.func_list.append(func)

        pass

    def simplify(self):
        for func in self.func_list:
            self.recursively_simplify(func)

        pass

    def recursively_simplify(self, func):
        var_list = []
        for symbol in func.time_complexity.free_symbols:
            target_func = self.get_function_by_name(str(symbol))
            if target_func:
                self.recursively_simplify(target_func)
                func.time_complexity = func.time_complexity.subs(symbol, target_func.time_complexity)
            else:
                var_list.append((symbol, sympy.oo))

        for param in func.parameter:
            var = sympy.Symbol(param.target.name)
            var_list.append((var, sympy.oo))

        func.time_complexity = func.time_complexity.simplify()
        if var_list:
            try:
                func.time_complexity = func.time_complexity.expand().expand(force=True)
                func.time_complexity = sympy.O(func.time_complexity, *var_list).args[0]
            except:
                pass
                # logging.exception("sympy can not simplify: ", func.time_complexity)
        else:
            func.time_complexity = sympy.O(func.time_complexity, *var_list).args[0]

        pass

    def get_function_by_name(self, target_name: str) -> FuncDeclNode:
        for function in self.func_list:
            if target_name == function.name:
                return function

    def get_function_complexity(self, target_name: str):
        for func in self.func_list:
            if target_name == func.name:
                return func.time_complexity
