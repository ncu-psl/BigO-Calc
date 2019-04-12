from sympy import Symbol, sqrt, Max

from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, BasicNode, IfNode
from bigo_ast.bigo_ast_visitor import BigOAstVisitor


class BigOEvaluator(BigOAstVisitor):

    def __init__(self, root: CompilationUnitNode):
        self.root = root

        pass

    def eval(self):
        super().visit(self.root)

        pass

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        if func_decl_node.determine_recursion():
            func_decl_node.time_complexity = 'is a recursive function'
        else:
            func_decl_node.time_complexity = self.visit_children(func_decl_node)

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

        if not big.isdigit():
            big = Symbol(big)
        else:
            big = int(big)

        if not small.isdigit():
            small = Symbol(small)
        else:
            small = int(small)

        if update == '++':
            for_node.time_complexity = big - small / 1
        elif update == '--':
            for_node.time_complexity = big - small / 1
        elif update == '*2':
            for_node.time_complexity = sqrt(big - small)
        elif update == '/2':
            for_node.time_complexity = sqrt(big - small)

        complexity = self.visit_children(for_node)
        if complexity:
            for_node.time_complexity *= complexity

        pass

    def visit_FuncCallNode(self, func_call: FuncCallNode):
        for func_decl in self.root.children:
            if func_call.name == func_decl.name:
                func_call.time_complexity = Symbol(func_decl.name)
                break

        pass

    def visit_IfNode(self, if_node: IfNode):
        if_node.condition.time_complexity = self.visit_children(if_node.condition)
        if_node.true_stmt.time_complexity = self.visit_children(if_node.true_stmt)
        if_node.false_stmt.time_complexity = self.visit_children(if_node.false_stmt)

        if not if_node.condition.time_complexity:
            if_node.condition.time_complexity = 1

        if not if_node.true_stmt.time_complexity:
            if_node.true_stmt.time_complexity = 1

        if not if_node.false_stmt.time_complexity:
            if_node.false_stmt.time_complexity = 1

        if_node.time_complexity = if_node.condition.time_complexity + Max(
            if_node.true_stmt.time_complexity,
            if_node.false_stmt.time_complexity)

        pass

    def visit_children(self, node: BasicNode):

        # evaluate children time complexity
        children_tc_list = []
        for child in node.children:
            super().visit(child)
            if child.time_complexity:
                children_tc_list.append(child.time_complexity)

        ans = 0
        for tc in children_tc_list:
            ans += tc

        return ans # '+'.join(str(tc) for tc in children_tc_list)
