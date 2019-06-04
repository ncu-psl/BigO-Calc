import copy
import logging

import sympy

from bigo_ast.bigo_ast import BasicNode, FuncDeclNode
from bigo_ast.bigo_ast_visitor import BigOAstVisitor


class BigOSimplify(BigOAstVisitor):
    def __init__(self, root: BasicNode):
        self.root = copy.deepcopy(root)

        # store simplified function (dynamic programming)
        self.simplified_function = []

        self.func_list = []
        for func in self.root.children:
            if type(func) == FuncDeclNode:
                self.func_list.append(func)

        pass

    def simplify(self):
        for func in self.func_list:
            self.visit_FuncDeclNode(func)

        return self.root

    def visit_FuncDeclNode(self, func: FuncDeclNode):
        if func in self.simplified_function:
            return func.time_complexity

        # expend function call
        for symbol in func.time_complexity.free_symbols:
            target_func = self.get_function_by_name(str(symbol))

            if target_func:
                if not target_func.recursive:
                    target_tc = self.visit_FuncDeclNode(target_func)

                    # substitute target function complexity into function
                    func.time_complexity = func.time_complexity.subs(symbol, target_tc)

        # get all symbol  (n, m, ...)
        var_list = set()
        for symbol in func.time_complexity.free_symbols:
            var_list.update([(symbol, sympy.oo)])

        # simplify time complexity
        func.time_complexity = func.time_complexity.expand()
        if var_list:
            try:
                func.time_complexity = sympy.O(func.time_complexity, *var_list).args[0]
            except:
                # SymPy cannot solve Max(n, log(n))
                # so we have to rewrite Max(a, b) to a + b then simplify it

                new_time_complexity = func.time_complexity.replace(sympy.Max, sympy.Add)
                logging.warning('in function ' + func.name + ':\nSymPy can not solve ' + str(
                    func.time_complexity) + ', we convert it into ' + str(
                    new_time_complexity))

                new_time_complexity = sympy.O(new_time_complexity, *var_list).args[0]
                func.time_complexity = new_time_complexity

        else:
            func.time_complexity = sympy.O(func.time_complexity).args[0]

        func.time_complexity = func.time_complexity.simplify()
        func.time_complexity = func.time_complexity.expand()

        self.simplified_function.append(func)
        return func.time_complexity

    def get_function_by_name(self, target_name: str) -> FuncDeclNode:
        for function in self.func_list:
            if target_name == function.name:
                return function

    def get_function_complexity(self, target_name: str):
        for func in self.func_list:
            if target_name == func.name:
                return func.time_complexity
