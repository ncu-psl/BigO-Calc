from pycparser.c_ast import FileAST, FuncDef, FuncCall, For, NodeVisitor, If

from ast_decorator.c.bigo_ast_node_factory import CFuncDeclNodeFactory, CForNodeFactory, CFuncCallNodeFactory, \
    CCompilationUnitNodeFactory, CIfNodeFactory


class CDecorateVisitor(NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None

        pass

    def visit_FileAST(self, pyc_file_ast: FileAST):
        self.cu = CCompilationUnitNodeFactory().create(pyc_file_ast)
        self.parent = self.cu

        for child in pyc_file_ast.ext:
            self.parent = self.cu
            self.visit(child)

        pass

    def visit_FuncDef(self, pyc_func_def: FuncDef):
        func_decl_node = CFuncDeclNodeFactory().create(pyc_func_def)
        self.parent.children.append(func_decl_node)

        for child in pyc_func_def.body.block_items:
            self.parent = func_decl_node
            self.visit(child)

        pass

    def visit_FuncCall(self, pyc_func_call: FuncCall):
        func_call_node = CFuncCallNodeFactory().create(pyc_func_call)
        self.parent.children.append(func_call_node)

        pass

    def visit_If(self, pyc_if: If):
        if_node = CIfNodeFactory().create(pyc_if)
        self.parent.children.append(if_node)

        for child in pyc_if.cond or []:
            self.parent = if_node.condition
            self.visit(child)

        for child in pyc_if.iftrue or []:
            self.parent = if_node.true_stmt
            self.visit(child)

        for child in pyc_if.iffalse or []:
            self.parent = if_node.false_stmt
            self.visit(child)

        pass

    def visit_For(self, pyc_for: For):
        for_node = CForNodeFactory().create(pyc_for)
        self.parent.children.append(for_node)

        self.parent = for_node
        if pyc_for.init is not None:
            self.visit(pyc_for.init)
        if pyc_for.next is not None:
            self.visit(pyc_for.next)
        if pyc_for.cond is not None:
            self.visit(pyc_for.cond)
        if pyc_for.stmt is not None:
            self.visit(pyc_for.stmt.block_items)

        pass

    def visit(self, node):
        super().visit(node)

        return self.cu
