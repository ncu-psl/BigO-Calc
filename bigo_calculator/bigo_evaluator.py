from BigOAST.BigOAST import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode
from BigOAST.bigo_ast_visitor import BigOAstVisitor


class BigOEvaluator(BigOAstVisitor):

    def __init__(self, root: CompilationUnitNode):
        self.root = root
        pass

    def eval(self):
        super().visit()
        FuncDeclEvaluator(self.root).visit()

        pass

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
            raise Exception("can not handle log")

        for child in for_node.children:
            super().visit(child)

        pass

    def visit_FuncCallNode(self, func_call: FuncCallNode):
        for func_decl in self.root.children:
            if func_call.name == func_decl.name:
                func_call.time_complexity = func_decl.name
                break

        pass


class FuncDeclEvaluator(BigOEvaluator):

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        for child in func_decl_node.children:
            func_decl_node.time_complexity += child.time_complexity + '+'
        func_decl_node.time_complexity = func_decl_node.time_complexity[:-1]

        for child in func_decl_node.children:
            super().visit(child)

        pass
