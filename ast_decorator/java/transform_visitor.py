from javalang.ast import Node
from javalang.tree import CompilationUnit, ForControl, MethodInvocation, MethodDeclaration, IfStatement, Literal, \
    MemberReference, BinaryOperation, VariableDeclarator, Assignment, ForStatement

from bigo_ast.bigo_ast import BasicNode, FuncDeclNode, \
    FuncCallNode, CompilationUnitNode, IfNode, ForNode, VariableNode, AssignNode, ConstantNode, Operator
from lib.node_visitor import NodeVisitor


class JavaTransformVisitor(NodeVisitor):
    def __init__(self):
        self.cu = None

        pass

    def transform(self, cu):
        # for path, node in cu:
        #    print(type(node))
        self.cu = self.visit(cu)
        return self.cu

    def visit_Literal(self, java_literal: Literal):
        constant_node = ConstantNode()
        self.set_coordinate(constant_node, java_literal)

        try:
            constant_node.value = int(java_literal.value)
        except:
            raise NotImplementedError('Constant type not support: ', java_literal.type)

        return constant_node

    def visit_BinaryOperation(self, java_op_node: BinaryOperation):
        operator_node = Operator()
        self.set_coordinate(operator_node, java_op_node)

        operator_node.op = java_op_node.operator
        operator_node.left = self.visit(java_op_node.operandl)
        operator_node.right = self.visit(java_op_node.operandr)

        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)

        return operator_node

    def visit_Assignment(self, java_assign: Assignment):
        assign_node = AssignNode()
        self.set_coordinate(assign_node, java_assign)

        op = java_assign.type
        if op != '=':
            raise NotImplementedError('op=', op)

        assign_node.target = self.visit(java_assign.expressionl)
        assign_node.value = self.visit(java_assign.value)

        return assign_node

    def visit_VariableDeclarator(self, java_var: VariableDeclarator):
        variable_node = VariableNode()
        self.set_coordinate(variable_node, java_var)
        variable_node.name = java_var.name

        return variable_node

    def visit_MemberReference(self, java_id: MemberReference):
        variable_node = VariableNode()
        self.set_coordinate(variable_node, java_id)
        variable_node.name = java_id.member

        return variable_node

    def visit_CompilationUnit(self, java_cu: CompilationUnit):
        self.cu = CompilationUnitNode()
        self.set_coordinate(self.cu, java_cu)

        if java_cu.types:
            for child in java_cu.types:
                self.cu.add_children(self.visit(child))

        return self.cu

    def visit_ClassDeclaration(self, java_class_def):
        stmts = []
        for stmt in java_class_def.body:
            stmts.append(self.visit(stmt))

        return stmts

    def visit_MethodDeclaration(self, java_method_decl: MethodDeclaration):
        func_decl_node = FuncDeclNode()
        self.set_coordinate(func_decl_node, java_method_decl)

        func_decl_node.name = java_method_decl.name
        if java_method_decl.parameters:
            for param in java_method_decl.parameters:
                func_decl_node.parameter.append(param.type.name + ' ' + param.name)

        for child in java_method_decl.body:
            func_decl_node.add_children(self.visit(child))

        return func_decl_node

    def visit_MethodInvocation(self, java_method_invocation: MethodInvocation):
        # func_call_node = JavaFuncCallNodeFactory().create(java_method_invocation)
        # self.parent.children.append(func_call_node)
        # func_call.copy_node_info_from(basic_node)

        func_call = FuncCallNode()
        self.set_coordinate(func_call, java_method_invocation)
        func_call.name = java_method_invocation.member
        if java_method_invocation.arguments:
            for arg in java_method_invocation.arguments:
                if type(arg) == Literal:
                    func_call.parameter.append(str(arg.value))
                elif type(arg) == MemberReference:
                    func_call.parameter.append(str(arg.member))
                elif type(arg) == BinaryOperation:
                    func_call.parameter.append(str(arg.operandl) + str(arg.operator) + str(arg.operandr))
                else:
                    func_call.parameter.append(str(arg))

        pass

    def visit_IfStatement(self, java_if_stmt: IfStatement):
        if_node = IfNode()
        self.set_coordinate(if_node, java_if_stmt)

        raise NotImplementedError()
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

    def visit_ForStatement(self, java_for_stmt: ForStatement):
        for_node = self.visit_ForControl(java_for_stmt.control)
        for child in java_for_stmt.body.statements:
            for_node.add_children(self.visit(child))

        return for_node

    def visit_ForControl(self, java_for_control: ForControl):
        for_node = ForNode()
        self.set_coordinate(for_node, java_for_control)

        for child in java_for_control.init:
            for_node.init.append(self.visit(child))

        raise NotImplementedError()
        term = self.visit(java_for_control.condition)

        update = self.visit(java_for_control.update)

        return for_node

    def generic_visit(self, node):
        if hasattr(node, 'children'):
            target = node.children
        elif type(node) is list or type(node) is tuple:
            target = node
        else:
            return

        children = []
        for c in target:
            child = self.visit(c)
            if child:
                if type(child) is list:
                    children.extend(child)
                else:
                    children.append(child)

        if children:
            return children


    @staticmethod
    def set_coordinate(node: BasicNode, java_node: Node):
        position = java_node.position
        if position:
            node.col = position.column
            node.line_number = position.line
