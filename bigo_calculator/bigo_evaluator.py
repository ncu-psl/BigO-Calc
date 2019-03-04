from BigOAST.BigOAST import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode
from BigOAST import BigOAstVisitor


class BigOEvaluator(BigOAstVisitor):

    def __init__(self, root: CompilationUnitNode):
        self.root = root
        pass

    def eval(self):
        ForEvaluator(self.root).visit()
        FuncDeclEvaluator(self.root).visit()
        FuncCallEvaluator(self.root).visit()

        super().visit()

        pass


class ForEvaluator(BigOEvaluator):

    def visit_ForNode(self, for_node: ForNode):
        init_value = for_node.init
        term_value = for_node.term
        update = for_node.next

        if term_value > init_value:
            small = init_value
            big = term_value
        else:
            small = term_value
            big = init_value

        if update == '++':
            for_node.time_complexity = '(' + big + '-' + small + ')' + '/1'
        elif update == '--':
            for_node.time_complexity = '(' + big + '-' + small + ')' + '/1'
        elif update == '/2':
            pass

        for child in for_node.children:
            super().visit(child)

        pass


class FuncDeclEvaluator(BigOEvaluator):

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        for child in func_decl_node.children:
            func_decl_node.time_complexity += child.time_complexity

        for child in func_decl_node.children:
            super().visit(child)

        pass


class FuncCallEvaluator(BigOEvaluator):

    def visit_FuncCallNode(self, func_call: FuncCallNode):
        for func_decl in self.root.children:
            if func_call.name == func_decl.name:
                if not func_decl.time_complexity:
                    FuncDeclEvaluator(self.root).visit(func_decl)
                func_call.time_complexity = func_decl.time_complexity
                break

        pass
