from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, BasicNode
from bigo_ast.bigo_ast_visitor import BigOAstVisitor


class BigOEvaluator(BigOAstVisitor):

    def __init__(self, root: CompilationUnitNode):
        self.root = root

        pass

    def eval(self):
        super().visit(self.root)

        pass

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        self.visit_children(func_decl_node)

        # trim redundant '*(' and ')'
        func_decl_node.time_complexity = func_decl_node.time_complexity[2:-1]

        pass

    def visit_ForNode(self, for_node: ForNode):
        init_value = for_node.init
        term_value = for_node.term
        update = for_node.update

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

        self.visit_children(for_node)

        pass

    def visit_FuncCallNode(self, func_call: FuncCallNode):
        for func_decl in self.root.children:
            if func_call.name == func_decl.name:
                func_call.time_complexity = '(' + func_decl.name + ')'
                break

        pass

    def visit_children(self, node: BasicNode):

        # evaluate children time complexity
        children_tc_list = []
        for child in node.children:
            super().visit(child)
            children_tc_list.append(child.time_complexity)

        if children_tc_list:
            node.time_complexity += '*(' + '+'.join(str(tc) for tc in children_tc_list) + ')'

        pass
