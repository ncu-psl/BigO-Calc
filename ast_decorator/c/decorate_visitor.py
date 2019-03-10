from pycparser.c_ast import NodeVisitor, FileAST, FuncDef, FuncCall, For

from ast_decorator.c.bigo_ast_node_factory import CFuncDeclNodeFactory, CForNodeFactory, CFuncCallNodeFactory, \
    CCompilationUnitNodeFactory


class CDecorateVisitor(NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None

        pass

    def visit_FileAST(self, file_ast: FileAST):
        self.cu = CCompilationUnitNodeFactory().create(file_ast)
        self.parent = self.cu

        for child in file_ast.ext:
            self.parent = self.cu
            self.visit(child)

        pass

    def visit_FuncDef(self, func_def: FuncDef):
        func_decl_node = CFuncDeclNodeFactory().create(func_def)
        self.parent.children.append(func_decl_node)

        for child in func_def.body.block_items:
            self.parent = func_decl_node
            self.visit(child)

        pass

    def visit_FuncCall(self, func_call: FuncCall):
        func_call_node = CFuncCallNodeFactory().create(func_call)
        self.parent.children.append(func_call_node)

        pass

    # def visit_If(self, node: If):
    #     if_node = IfNode(node)
    #     self.parent.children.append(if_node)
    #
    #     if node.cond is not None: self.visit(node.cond)
    #     if node.iftrue is not None:  self.visit(node.iftrue)
    #     if node.iffalse is not None: self.visit(node.iffalse)
    #
    #     pass

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
        pass
