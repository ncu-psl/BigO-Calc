from BigOAST.bigo_ast_visitor import BigOASTVisitor
from BigOAST.for_node import ForNode
from BigOAST.func_call_node import FuncCallNode
from BigOAST.func_decl_node import FuncDeclNode


class TimeComplexityCalculateVisitor(BigOASTVisitor):

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        print('[%s]' % func_decl_node.name)

        for child in func_decl_node:
            self.visit(child)

        pass

    def visit_FuncCallNode(self, func_call_node: FuncCallNode):
        print('    ', func_call_node.name)

        pass

    def visit_ForNode(self, for_node: ForNode):
        print('init: %s, term: %s, update: %s' % (for_node.init, for_node.term, for_node.next))

        pass

    def check_recursion(self):
        func_decl_list = self.root.children
        for func_decl in func_decl_list:
            func_decl.determine_recursion()
            # if func_decl.determine_recursion():
            # print(func_decl.name)
        pass

    def calculate(self):
        self.root.add_parent_to_children()

        self.check_recursion()
        self.visit(self.root)

        pass
