import sympy
from sympy import O

from bigo_ast.bigo_ast import BasicNode, FuncDeclNode
from bigo_ast.bigo_ast_visitor import BigOAstVisitor


class BigOSimplify(BigOAstVisitor):
    def __init__(self, root: BasicNode):
        self.root = root
        pass

    def simplify(self):
        func_dict = {}
        for func in self.root.children:
            if type(func) == FuncDeclNode:
                func_dict.update({sympy.Symbol(func.name): func.time_complexity})

        for func in self.root.children:
            if type(func) != FuncDeclNode:
                continue
            symbol_set = func.time_complexity.free_symbols

            var_list = []
            for symbol in symbol_set:
                symbol_complexity = func_dict.get(symbol)
                if symbol_complexity:
                    func.time_complexity = func.time_complexity.subs(symbol, symbol_complexity)
                else:
                    var_list.append(symbol)

            func.time_complexity = func.time_complexity.simplify()
            if var_list:
                try:
                    func.time_complexity = func.time_complexity.expand().expand(force=True)
                    func.time_complexity = O(func.time_complexity, (var_list[0], sympy.oo)).args[0]
                except:
                    pass
                    # logging.exception("sympy can not simplify: ", func.time_complexity)
            else:
                func.time_complexity = O(func.time_complexity)

        pass
