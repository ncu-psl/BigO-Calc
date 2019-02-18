from pycparser.c_ast import NodeVisitor, FuncCall, FuncDef, For, FileAST

from BigOAST.basic_node import BasicNode
from BigOAST.compilation_unit_node import CompilationUnitNode
from BigOAST.for_node import ForNode
from BigOAST.func_call_node import FuncCallNode
from BigOAST.func_decl_node import FuncDeclNode


class Decorator(NodeVisitor):
    def __init__(self):
        self.parent = BasicNode()
        self.cu = None

        pass

    def visit_FileAST(self, file_ast: FileAST):
        self.cu = CompilationUnitNode(file_ast)
        self.parent = self.cu

        for child in file_ast.ext:
            self.parent = self.cu
            self.visit(child)

        pass

    def visit_FuncDef(self, func_def: FuncDef):
        func_decl_node = FuncDeclNode(func_def)
        self.parent.children.append(func_decl_node)

        for child in func_def.body.block_items:
            self.parent = func_decl_node
            self.visit(child)

        pass

    def visit_FuncCall(self, func_call: FuncCall):
        func_call_node = FuncCallNode(func_call)
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

    def visit_For(self, node: For):
        for_node = ForNode(node)
        self.parent.children.append(for_node)

        for child in node.stmt.block_items:
            self.parent = for_node
            self.visit(child)

        pass

    def decorate(self, ast: FileAST):
        self.visit(ast)

        return self.cu
