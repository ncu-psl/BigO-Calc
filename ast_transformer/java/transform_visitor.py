from javalang.ast import Node
from javalang.tree import CompilationUnit, ForControl, MethodInvocation, MethodDeclaration, IfStatement, Literal, \
    MemberReference, BinaryOperation, VariableDeclarator, Assignment, ForStatement

from bigo_ast.bigo_ast import FuncDeclNode, \
    FuncCallNode, CompilationUnitNode, IfNode, ForNode, VariableNode, AssignNode, ConstantNode, Operator, BasicNode
from lib.node_visitor import NodeVisitor


class JavaTransformVisitor(NodeVisitor):
    def __init__(self):
        self.cu = None

        pass

    def transform(self, cu):
        self.cu = self.visit(cu)

        return self.cu

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
                # func_decl_node.parameter.append(param.type.name + ' ' + param.name)
                func_decl_node.parameter.append(self.visit_VariableDeclarator(param))

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

        return func_call

    def visit_VariableDeclarator(self, java_var: VariableDeclarator):
        assign_node = AssignNode()
        self.set_coordinate(assign_node, java_var)

        variable_node = VariableNode()
        self.set_coordinate(variable_node, java_var)

        # target
        variable_node.name = java_var.name
        assign_node.target = variable_node

        # value
        if hasattr(java_var, 'initializer'):
            if java_var.initializer:
                assign_node.value = self.visit(java_var.initializer)

        return assign_node

    def visit_MemberReference(self, java_id: MemberReference):
        variable_node = VariableNode()
        self.set_coordinate(variable_node, java_id)
        variable_node.name = java_id.member

        pre_opr = java_id.prefix_operators
        pos_opr = java_id.postfix_operators

        # need to do some trick of ++i, i++
        if pre_opr or pos_opr:
            if len(pre_opr) > 1 or len(pos_opr) > 1:
                raise NotImplementedError()

            # create a new id and clean prefix, posfix
            new_id = java_id
            new_id.prefix_operators = []
            new_id.postfix_operators = []

            # create a new binary operator
            binopr = BinaryOperation()
            binopr.operandl = new_id

            # create a new Literal
            binopr.operandr = Literal()
            binopr.operandr.value = '1'
            binopr.prefix_operators = []
            binopr.postfix_operators = []

            # get operator
            if len(pre_opr) == 1:
                if pre_opr[0] == '++':
                    binopr.operator = '+'
                elif pre_opr[0] == '--':
                    binopr.operator = '-'
            elif len(pos_opr) == 1:
                if pos_opr[0] == '++':
                    binopr.operator = '+'
                elif pos_opr[0] == '--':
                    binopr.operator = '-'

            # convert into Assignment
            assign = Assignment()
            assign.type = '='
            assign.expressionl = new_id
            assign.value = binopr

            return self.visit(assign)

        return variable_node

    def visit_Literal(self, java_literal: Literal):
        constant_node = ConstantNode()
        self.set_coordinate(constant_node, java_literal)

        try:
            constant_node.value = int(java_literal.value)
        except:

            if java_literal.value == 'true':
                constant_node.value = 1
            elif java_literal.value == 'false':
                constant_node.value = 0
            else:
                raise NotImplementedError('Constant type not support: ', java_literal)

        return constant_node

    def visit_Assignment(self, java_assign: Assignment):
        assign_node = AssignNode()
        self.set_coordinate(assign_node, java_assign)

        # need to do some trick of +=, -=, *=, /=
        if len(java_assign.type) > 1:
            op = java_assign.type[:-1]
            if op == '+' or op == '-' or op == '*' or op == '/':
                new_op = BinaryOperation()
                self.set_coordinate(new_op, java_assign)

                new_op.operator = op
                new_op.operandl = java_assign.expressionl
                new_op.operandr = java_assign.value
            else:
                raise Exception("does not support operator: ", java_assign.op)
            java_assign.type = '='
            java_assign.value = new_op

        assign_node.target = self.visit(java_assign.expressionl)
        assign_node.value = self.visit(java_assign.value)

        return assign_node

    def visit_BinaryOperation(self, java_op_node: BinaryOperation):
        operator_node = Operator()
        self.set_coordinate(operator_node, java_op_node)

        operator_node.op = java_op_node.operator
        operator_node.left = self.visit(java_op_node.operandl)
        operator_node.right = self.visit(java_op_node.operandr)

        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)

        return operator_node

    def visit_IfStatement(self, java_if: IfStatement):
        if_node = IfNode()
        self.set_coordinate(if_node, java_if)

        # condition
        if_node.condition = self.visit(java_if.condition)

        # true stmt
        if hasattr(java_if.then_statement, 'statements'):
            true_stmt = java_if.then_statement.statements
        else:
            true_stmt = java_if.then_statement.expression

        for stmt in true_stmt:
            child = self.visit(stmt)
            if type(child) is not list:
                child = [child]
            if_node.true_stmt.extend(child)

        # false stmt
        if java_if.else_statement:
            if hasattr(java_if.then_statement, 'statements'):
                false_stmt = java_if.else_statement.statements
            else:
                false_stmt = java_if.else_statement.expression

            for stmt in false_stmt:
                child = self.visit(stmt)
                if type(child) is not list:
                    child = [child]
                if_node.false_stmt.extend(child)

        return if_node

    def visit_ForStatement(self, java_for_stmt: ForStatement):
        for_node = self.visit_ForControl(java_for_stmt.control)

        if type(java_for_stmt.body) is not list:
            java_for_stmt.body = [java_for_stmt.body]

        for child in java_for_stmt.body:
            for_node.add_children(self.visit(child))

        return for_node

    def visit_ForControl(self, java_for_control: ForControl):
        for_node = ForNode()
        self.set_coordinate(for_node, java_for_control)

        if type(java_for_control.init) is not list:
            java_for_control.init = [java_for_control.init]

        for child in java_for_control.init:
            init = self.visit(child)
            if type(init) is list:
                for_node.init.extend(init)
            else:
                for_node.init.append(init)

        for_node.term = self.visit(java_for_control.condition)

        if type(java_for_control.update) is not list:
            java_for_control.update = [java_for_control.update]
        for child in java_for_control.update:
            update = self.visit(child)
            if type(update) is list:
                for_node.update.extend(update)
            else:
                for_node.update.append(update)

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

        pass
