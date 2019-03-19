from lib.node_visitor import NodeVisitor

from javalang.ast import Node
from javalang.tree import CompilationUnit, ForControl, MethodInvocation, MethodDeclaration

from ast_decorator.java.bigo_ast_node_factory import JavaCompilationUnitNodeFactory, JavaFuncCallNodeFactory, \
    JavaFuncDeclNodeFactory, JavaForNodeFactory


class JavaDecorateVisitor(NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None

        pass

    def visit_CompilationUnit(self, java_cu: CompilationUnit):
        self.cu = JavaCompilationUnitNodeFactory().create(java_cu)
        self.parent = self.cu

        if java_cu.types:
            for child in java_cu.types:
                self.parent = self.cu
                self.visit(child)

        pass

    def visit_ClassDeclaration(self, class_def: Node):
        for child in class_def.body:
            self.parent = self.cu
            self.visit(child)

        pass

    def visit_MethodDeclaration(self, java_method_decl: MethodDeclaration):
        func_decl_node = JavaFuncDeclNodeFactory().create(java_method_decl)
        self.parent.children.append(func_decl_node)

        for child in java_method_decl.body:
            self.parent = func_decl_node
            self.visit(child)

        pass

    def visit_MethodInvocation(self, java_method_invocation: MethodInvocation):
        func_call_node = JavaFuncCallNodeFactory().create(java_method_invocation)
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

    def visit_ForControl(self, java_for_control: ForControl):
        for_node = JavaForNodeFactory().create(java_for_control)
        self.parent.children.append(for_node)

        self.parent = for_node

        pass

    def visit(self, node):
        super().visit(node)

        return self.cu
