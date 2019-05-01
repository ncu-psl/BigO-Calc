from pycparser.c_ast import FileAST, FuncDef, FuncCall, For, NodeVisitor, If, ID, Assignment, Constant, BinaryOp, \
    UnaryOp, Decl

from bigo_ast.bigo_ast import WhileNode, BasicNode, VariableNode, ConstantNode, AssignNode, Operator, FuncDeclNode, \
    FuncCallNode, CompilationUnitNode, IfNode, ForNode


class CDecorateVisitor(NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None

        pass

    def visit_ID(self, pyc_id: ID):
        variable_node = VariableNode()
        self.set_coordinate(variable_node, pyc_id.coord)
        variable_node.name = pyc_id.name

        self.parent = variable_node
        for child in pyc_id:
            self.visit(child)

        return variable_node

    def visit_Constant(self, pyc_constant: Constant):
        constant_node = ConstantNode()
        self.set_coordinate(constant_node, pyc_constant.coord)
        if pyc_constant.type == 'int':
            constant_node.value = int(pyc_constant.value)
        else:
            raise NotImplementedError('Constant type not support: ', pyc_constant.type)

        return constant_node

    def visit_BinaryOp(self, pyc_bin_op: BinaryOp):
        operator_node = Operator()
        self.set_coordinate(operator_node, pyc_bin_op.coord)
        operator_node.op = pyc_bin_op.op
        operator_node.left = self.visit(pyc_bin_op.left)
        operator_node.right = self.visit(pyc_bin_op.right)

        if operator_node.left is not list:
            operator_node.children.append(operator_node.left)
        else:
            operator_node.children.extend(operator_node.left)

        if operator_node.right is not list:
            operator_node.children.append(operator_node.right)
        else:
            operator_node.children.extend(operator_node.right)

        return operator_node

    def visit_UnaryOp(self, pyc_unary_op: UnaryOp):
        # convert pyc_unary operator to pyc_assignment
        op = pyc_unary_op.op
        if op == '++' or op == 'p++':
            op = '+'
        elif op == '--' or op == 'p--':
            op = '-'
        # else:
        #    raise NotImplementedError('op=', op)

        right = BinaryOp(op, pyc_unary_op.expr, Constant('int', 1))
        pyc_assign = Assignment('=', pyc_unary_op.expr, right)

        return self.visit(pyc_assign)

    def visit_Assignment(self, pyc_assign: Assignment):
        # need to do some trick of +=, -=, *=, /=
        if len(pyc_assign.op) > 1:
            op = pyc_assign.op[:-1]
            if op == '+' or op == '-' or op == '*' or op == '/':
                new_op = BinaryOp(op, pyc_assign.lvalue, pyc_assign.rvalue)
            else:
                raise Exception("does not support operator: ", pyc_assign.op)
            pyc_assign.op = '='
            pyc_assign.rvalue = new_op

        # create Big-O AST assign node
        assign_node = AssignNode()
        self.set_coordinate(assign_node, pyc_assign.coord)
        assign_node.target = self.visit(pyc_assign.lvalue)
        assign_node.value = self.visit(pyc_assign.rvalue)

        assign_node.children.append(assign_node.target)
        assign_node.children.append(assign_node.value)

        return assign_node

    def visit_Decl(self, pyc_decl: Decl):
        assign_node = AssignNode()
        self.set_coordinate(assign_node, pyc_decl.coord)
        variable = VariableNode()
        variable.name = pyc_decl.name
        assign_node.target = variable
        if pyc_decl.init:
            # if hasattr(pyc_decl.init, 'value'):
            assign_node.value = self.visit(pyc_decl.init)

        return assign_node

    def visit_FileAST(self, pyc_file_ast: FileAST):
        self.cu = CompilationUnitNode()
        self.set_coordinate(self.cu, pyc_file_ast.coord)

        for child in pyc_file_ast.ext:
            self.parent = self.cu
            func = self.visit(child)
            if func:
                self.cu.children.append(func)

        pass

    def visit_FuncDef(self, pyc_func_def: FuncDef):
        func_decl_node = FuncDeclNode()
        self.set_coordinate(func_decl_node, pyc_func_def.coord)
        func_decl_node.name = pyc_func_def.decl.name
        if pyc_func_def.decl.type.args:
            param_list = pyc_func_def.decl.type.args.params
            for param in param_list:
                func_decl_node.parameter.append(param.type.type.names[0] + ' ' + param.name)

        for child in pyc_func_def.body.block_items:
            self.parent = func_decl_node
            stmt = self.visit(child)
            if stmt:
                if type(stmt) is list:
                    func_decl_node.children.extend(stmt)
                else:
                    func_decl_node.children.append(stmt)

        return func_decl_node

    def visit_FuncCall(self, pyc_func_call: FuncCall):
        func_call_node = FuncCallNode()
        self.set_coordinate(func_call_node, pyc_func_call.coord)
        func_call_node.name = pyc_func_call.name.name
        if pyc_func_call.args:
            for param in pyc_func_call.args.exprs:
                if isinstance(param, Constant):
                    func_call_node.parameter.append(param.value)
                elif isinstance(param, ID):
                    func_call_node.parameter.append(param.name)

        return func_call_node

    def visit_If(self, pyc_if: If):
        if_node = IfNode()
        self.set_coordinate(if_node, pyc_if.coord)

        if_node.condition = self.visit(pyc_if.cond)

        self.parent = if_node.true_stmt
        for child in pyc_if.iftrue or []:
            child_node = self.visit(child)
            if type(child_node) is list:
                if_node.true_stmt.extend(child_node)
            else:
                if_node.true_stmt.append(child_node)

        self.parent = if_node.true_stmt
        for child in pyc_if.iffalse or []:
            child_node = self.visit(child)
            if type(child_node) is list:
                if_node.false_stmt.extend(child_node)
            else:
                if_node.false_stmt.append(child_node)

        if_node.children.extend(if_node.true_stmt)
        if_node.children.extend(if_node.false_stmt)

        return if_node

    def visit_For(self, pyc_for: For):
        # convert pyc_for to while
        # self.while_converter(pyc_for)

        for_node = ForNode()
        self.set_coordinate(for_node, pyc_for.coord)

        init = self.visit(pyc_for.init)
        if type(init) is list:
            for_node.init.extend(init)
        else:
            for_node.init.append(init)

        for_node.term = self.visit(pyc_for.cond)

        update = self.visit(pyc_for.next)
        if type(update) is list:
            for_node.update.extend(update)
        else:
            for_node.update.append(update)

        for child in pyc_for.stmt or []:
            child_node = self.visit(child)
            if child_node is list:
                for_node.children.extend(child_node)
            else:
                for_node.children.append(child_node)

        return for_node

    def generic_visit(self, node):
        children = []
        for c in node:
            child = self.visit(c)
            if child:
                children.append(child)

        if children:
            return children

    def decorate(self, root):
        self.visit(root)
        return self.cu

    @staticmethod
    def set_coordinate(node: BasicNode, coord):
        if coord:
            node.col = coord.column
            node.line_number = coord.line

    def while_converter(self, pyc_for: For):
        # use pyc_for to generate while_node
        while_node = WhileNode()

        # termination
        self.parent = while_node
        while_node.term = self.visit(pyc_for.cond)

        # body
        for child in pyc_for.stmt.block_items:
            while_node.children.extend(self.visit(child))

        # update
        while_node.children.extend(self.visit(pyc_for.next))

        # return initialization and while
        return [self.visit(pyc_for.init), while_node]
