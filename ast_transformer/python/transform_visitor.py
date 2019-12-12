from ast import Module, FunctionDef, Call, Starred, Assign, AnnAssign, AugAssign,\
    BinOp, Add, Sub, Mult, Div, Num, Name
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from bigo_ast.bigo_ast import WhileNode, BasicNode, VariableNode, ConstantNode, AssignNode, Operator, FuncDeclNode, \
    FuncCallNode, CompilationUnitNode, IfNode, ForNode

class PyTransformVisitor(BigOAstVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None

        pass

    def transform(self, root):
        self.visit(root)
        return self.cu

    def visit_Module(self, ast_module: Module):
        self.cu = CompilationUnitNode()
        self.set_coordinate(self.cu, ast_module.coord)

        for child in ast_module.body:
            self.parent = self.cu
            self.cu.add_children(self.visit(child))

        pass

    def visit_FunctionDef(self, ast_func_def: FunctionDef):
        func_decl_node = FuncDeclNode()
        self.set_coordinate(func_decl_node, ast_func_def.coord)
        func_decl_node.name = ast_func_def.name
        # arg
        if ast_func_def.args.args:
            args_list = ast_func_def.args.args
            for arg in args_list:
                func_decl_node.parameter.append(arg.arg)
        #kwonlyarg
        if ast_func_def.args.kwonlyargs:
            kwonlyargs_list = ast_func_def.args.kwonlyargs
            for kwonlyarg in kwonlyargs_list:
                func_decl_node.parameter.append(kwonlyarg.arg)
        #vararg
        if ast_func_def.args.vararg:
            func_decl_node.parameter.append(ast_func_def.args.vararg.arg)
        #kwarg
        if ast_func_def.args.kwarg:
            func_decl_node.parameter.append(ast_func_def.args.kwarg.arg)

        for child in ast_func_def.body:
            self.parent = func_decl_node
            func_decl_node.add_children(self.visit(child))

        return func_decl_node

    #先做3.5版
    def visit_Call(self, ast_call: Call):
        func_call_node = FuncCallNode()
        self.set_coordinate(func_call_node, ast_call.coord)
        func_call_node.name = ast_call.func.id

        if ast_call.args:
            for arg in ast_call.args:
                if type(arg) == Starred:
                    func_call_node.parameter.append(arg.value.id)
                else:
                    func_call_node.parameter.append(arg.id)

        if ast_call.keywords:
            for keyword in ast_call.keywords:
                if keyword.arg == None:
                    func_call_node.parameter.append(keyword.value.id)
                else:
                    func_call_node.parameter.append(keyword.arg)
        return func_call_node

    
    def visit_Name(self, ast_name: Name):
        variable_node = VariableNode()
        self.set_coordinate(variable_node, ast_name.coord)
        variable_node.name = ast_name.id

        return variable_node

    def visit_Cast(self, cast: Cast):
        return self.visit(cast.expr)

    def visit_ArrayRef(self, pyc_arr_ref: ArrayRef):
        variable_node = VariableNode()
        self.set_coordinate(variable_node, pyc_arr_ref.coord)

        # add all index into variable_node.children
        pyc_arr = pyc_arr_ref
        while type(pyc_arr) == ArrayRef:
            variable_node.add_children(self.visit(pyc_arr.subscript))
            pyc_arr = pyc_arr.name

        # ArrayRef variable name will store in the last attr pyc_arr_ref.name.name...name
        variable_node.name = pyc_arr.name

        return variable_node

    def visit_Num(self, ast_num: Num):
        constant_node = ConstantNode()
        self.set_coordinate(constant_node, ast_num.coord)
        if type(ast_num.n) == int:
            constant_node.value = ast_num.n
        # else:
        #     raise NotImplementedError('Constant type not support: ', pyc_constant.type)

        return constant_node

    def visit_Assign(self, ast_assign: Assign):
        # create Big-O AST assign node
        assign_node = AssignNode()
        self.set_coordinate(assign_node, ast_assign.coord)
        assign_node.target = self.visit(ast_assign.targets[0])
        assign_node.value = self.visit(ast_assign.value)

        return assign_node

    def visit_AnnAssign(self, ast_ann_assign: AnnAssign):
        # create Big-O AST assign node
        assign_node = AssignNode()
        self.set_coordinate(assign_node, ast_assign.coord)
        assign_node.target = self.visit(ast_assign.targets[0])
        assign_node.value = self.visit(ast_assign.value)

        return assign_node

    def visit_AugAssign(self, ast_aug_assign: AugAssign):
        # need to do some trick of +=, -=, *=, /=
        if type(ast_aug_assign.op) == Add:
            new_op = BinOp(ast_aug_assign.target, Add(), ast_aug_assign.value)
        elif type(ast_aug_assign.op) == Sub:
            new_op = BinOp(ast_aug_assign.target, Sub(), ast_aug_assign.value)
        elif type(ast_aug_assign.op) == Mult:
            new_op = BinOp(ast_aug_assign.target, Mult(), ast_aug_assign.value)
        elif type(ast_aug_assign.op) == Div:
            new_op = BinOp(ast_aug_assign.target, Div(), ast_aug_assign.value)
        else:
            raise Exception("does not support operator: ", ast_aug_assign.op)
        ast_assign = Assign(ast_aug_assign.target, new_op)

        # create Big-O AST assign node
        assign_node = AssignNode()
        self.set_coordinate(assign_node, ast_aug_assign.coord)
        assign_node.target = self.visit(ast_assign.target)
        assign_node.value = self.visit(ast_assign.value)

        return assign_node

    def visit_BinOp(self, ast_bin_op: BinOp):
        operator_node = Operator()
        self.set_coordinate(operator_node, ast_bin_op.coord)
        if type(ast_aug_assign.op) == Add:
            operator_node.op = '+'
        elif type(ast_aug_assign.op) == Sub:
            operator_node.op = '-'
        elif type(ast_aug_assign.op) == Mult:
            operator_node.op = '*'
        elif type(ast_aug_assign.op) == Div:
            operator_node.op = '/'
        elif type(ast_aug_assign.op) == FloorDiv:
            operator_node.op = '//'
        elif type(ast_aug_assign.op) == Mod:
            operator_node.op = '%'
        elif type(ast_aug_assign.op) == Pow:
            operator_node.op = '**'
        elif type(ast_aug_assign.op) == LShift:
            operator_node.op = '<<'
        elif type(ast_aug_assign.op) == RShift:
            operator_node.op = '>>'
        elif type(ast_aug_assign.op) == BitOr:
            operator_node.op = '|'
        elif type(ast_aug_assign.op) == BitAnd:
            operator_node.op = '&'
        elif type(ast_aug_assign.op) == MatMult:
            operator_node.op = '@'
        else:
            raise Exception("does not support operator: ", ast_aug_assign.op)
        operator_node.left = self.visit(ast_bin_op.left)
        operator_node.right = self.visit(ast_bin_op.right)

        # need to do some trick at signed variable (-1, +1, -n, +n)
        if hasattr(pyc_bin_op.right, 'value'):
            if pyc_bin_op.left.coord == pyc_bin_op.right.coord:
                if type(pyc_bin_op.left) == Constant and type(pyc_bin_op.right) == Constant:
                    zero = ConstantNode()
                    self.set_coordinate(zero, pyc_bin_op.coord)
                    zero.value = 0

                    operator_node.right = operator_node.left
                    operator_node.left = zero

        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)

        return operator_node

    def visit_UnaryOp(self, pyc_unary_op: UnaryOp):
        # convert pyc_unary operator to pyc_assignment
        op = pyc_unary_op.op
        if op == '++' or op == 'p++':
            op = '+'
        elif op == '--' or op == 'p--':
            op = '-'
        elif op == '+' or op == '-':
            bin_op = BinaryOp(op, Constant('int', '0', pyc_unary_op.coord), pyc_unary_op.expr, pyc_unary_op.coord)
            return self.visit(bin_op)
        # else:
        #     raise NotImplementedError('op=', op)
        right = BinaryOp(op, pyc_unary_op.expr, Constant('int', '1', pyc_unary_op.coord), pyc_unary_op.coord)
        pyc_assign = Assignment('=', pyc_unary_op.expr, right, pyc_unary_op.coord)

        return self.visit(pyc_assign)

    def visit_If(self, pyc_if: If):
        if_node = IfNode()
        self.set_coordinate(if_node, pyc_if.coord)

        # condition
        if_node.condition = self.visit(pyc_if.cond)

        # convert pyc true statement to list
        if type(pyc_if.iftrue) is not list:
            pyc_if.iftrue = [pyc_if.iftrue]

        self.parent = if_node.true_stmt
        for child in pyc_if.iftrue or []:
            child_node = self.visit(child)
            if child_node:
                if type(child_node) is list:
                    if_node.true_stmt.extend(child_node)
                else:
                    if_node.true_stmt.append(child_node)

        # convert pyc false statement to list
        if pyc_if.iffalse:
            if type(pyc_if.iffalse) is not list:
                pyc_if.iffalse = [pyc_if.iffalse]

            self.parent = if_node.false_stmt
            for child in pyc_if.iffalse or []:
                child_node = self.visit(child)
                if child_node:
                    if type(child_node) is list:
                        if_node.false_stmt.extend(child_node)
                    else:
                        if_node.false_stmt.append(child_node)

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

        if type(pyc_for.stmt) is not list:
            pyc_for.stmt = [pyc_for.stmt]

        for child in pyc_for.stmt:
            child_node = self.visit(child)
            for_node.add_children(child_node)

        return for_node

    def generic_visit(self, node):
        children = []
        for c in node:
            child = self.visit(c)
            if child:
                if type(child) is list:
                    children.extend(child)
                else:
                    children.append(child)

        if children:
            return children

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
            while_node.add_children(self.visit(child))

        # update
        while_node.add_children(self.visit(pyc_for.next))

        # return initialization and while
        return [self.visit(pyc_for.init), while_node]
