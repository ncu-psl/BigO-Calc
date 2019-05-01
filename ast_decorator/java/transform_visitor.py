from javalang.ast import Node
from javalang.tree import CompilationUnit, ForControl, MethodInvocation, MethodDeclaration, IfStatement

from ast_decorator.java.bigo_ast_node_factory import JavaCompilationUnitNodeFactory, JavaFuncCallNodeFactory, \
    JavaFuncDeclNodeFactory, JavaForNodeFactory, JavaIfNodeFactory
from lib.node_visitor import NodeVisitor


class JavaTransformVisitor(NodeVisitor):
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

    def visit_ClassDeclaration(self, java_class_def: Node):
        for child in java_class_def.body:
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

    def visit_IfStatement(self, java_if_stmt: IfStatement):
        if_node = JavaIfNodeFactory().create(java_if_stmt)
        self.parent.children.append(if_node)

        for child in java_if_stmt.condition or []:
            self.parent = if_node.condition
            self.visit(child)

        if java_if_stmt.then_statement and hasattr(java_if_stmt.then_statement, 'statements'):
            for child in java_if_stmt.then_statement.statements or []:
                self.parent = if_node.true_stmt
                self.visit(child)

        if java_if_stmt.else_statement and hasattr(java_if_stmt.else_statement, 'statements'):
            for child in java_if_stmt.else_statement.statements or []:
                self.parent = if_node.false_stmt
                self.visit(child)

        pass

    def visit_ForControl(self, java_for_control: ForControl):
        for_node = JavaForNodeFactory().create(java_for_control)
        self.parent.children.append(for_node)

        self.parent = for_node

        pass

    def visit(self, node):
        super().visit(node)

        return self.cu
