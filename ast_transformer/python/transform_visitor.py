from ast import Module, FunctionDef, Call, Starred, Assign, AnnAssign, AugAssign,\
    BinOp, BoolOp, And, Or, Add, Sub, Mult, FloorDiv, Pow, Mod, Div, Num, Name, If, For, NodeVisitor, iter_fields, AST, Compare
import ast
from bigo_ast.bigo_ast import WhileNode, BasicNode, VariableNode, ConstantNode, AssignNode, Operator, FuncDeclNode, \
    FuncCallNode, CompilationUnitNode, IfNode, ForNode

class PyTransformVisitor(NodeVisitor):
    def __init__(self):
        self.parent = None
        self.cu = None

        pass

    def transform(self, root):
        self.visit(root)
        return self.cu

    def visit_Module(self, ast_module: Module):
        self.cu = CompilationUnitNode()
        # coord = coordinate( ast_module.col_offset, ast_module.lineno)
        # self.set_coordinate(self.cu, coord)
        for child in ast_module.body:
            self.parent = self.cu
            self.cu.add_children(self.visit(child))

        pass

    def visit_FunctionDef(self, ast_func_def: FunctionDef):
        func_decl_node = FuncDeclNode()
        # coord = coordinate(ast_func_def.col_offset, ast_func_def.lineno)
        # self.set_coordinate(func_decl_node, coord)
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
        # coord = coordinate(ast_call.col_offset, ast_call.lineno)
        # self.set_coordinate(func_call_node, coord)
        if hasattr(ast_call.func,'id'):
            func_call_node.name = ast_call.func.id
        else:
            func_call_node.name = ast_call.func.attr

        # if ast_call.args:
        #     for arg in ast_call.args:
        #         if(hasattr(arg,'value')):
        #             if type(arg) == Starred:
        #                 func_call_node.parameter.append(arg.value.id)
        #             else:
        #                 func_call_node.parameter.append(arg.id)

        # if ast_call.keywords:
        #     for keyword in ast_call.keywords:
        #         if(hasattr(keyword,'value')):
        #             if keyword.arg == None:
        #                 func_call_node.parameter.append(keyword.value.id)
        #             else:
        #                 func_call_node.parameter.append(keyword.arg)
        return func_call_node

    
    def visit_Name(self, ast_name: Name):
        variable_node = VariableNode()
        # coord = coordinate(ast_name.col_offset, ast_name.lineno)
        # self.set_coordinate(variable_node, coord)
        variable_node.name = ast_name.id

        return variable_node

    def visit_Num(self, ast_num: Num):
        constant_node = ConstantNode()
        # coord = coordinate(ast_num.col_offset, ast_num.lineno)
        # self.set_coordinate(constant_node, coord) 
        if type(ast_num.n) == int:
            constant_node.value = ast_num.n
        # else:
        #     raise NotImplementedError('Constant type not support: ', type(ast_num.n))

        return constant_node

    def visit_Assign(self, ast_assign: Assign):
        # create Big-O AST assign node
        assign_node = AssignNode()
        # coord = coordinate(ast_assign.col_offset, ast_assign.lineno)
        # self.set_coordinate(assign_node, coord) 
        assign_node.target = self.visit(ast_assign.targets[0])
        assign_node.value = self.visit(ast_assign.value)

        return assign_node

    def visit_AnnAssign(self, ast_ann_assign: AnnAssign):
        # create Big-O AST assign node
        assign_node = AssignNode()
        # coord = coordinate(ast_ann_assign.col_offset, ast_ann_assign.lineno)
        # self.set_coordinate(assign_node, coord)
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
        # coord = coordinate(ast_aug_assign.col_offset, ast_aug_assign.lineno)
        # self.set_coordinate(assign_node, coord)
        assign_node.target = self.visit(ast_assign.targets)
        assign_node.value = self.visit(ast_assign.value)

        return assign_node
    def visit_BoolOp(self, ast_bool_op: BoolOp):
        operator_node = Operator()
        if type(ast_bool_op.op) == And:
            op = '=='
        elif type(ast_bool_op.op) == Or:
            op = '||'
        else:
            raise Exception("does not support operator: ", ast_bool_op.op)

        right = BasicNode()
        right_flag = False
        for node in reversed(ast_bool_op.values):
            if right_flag == False:
                right = self.visit(node)
                right_flag == True
            else:
                left = self.visit(node)
                operator_node = Operator()
                operator.op = op
                operator.right = right
                operator.left = left
                right = operator

        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)
        return operator_node

    def visit_BinOp(self, ast_bin_op: BinOp):
        operator_node = Operator()
        # coord = coordinate(ast_bin_op.col_offset, ast_bin_op.lineno)
        # self.set_coordinate(operator_node, coord)
        if type(ast_bin_op.op) == Add:
            operator_node.op = '+'
        elif type(ast_bin_op.op) == Sub:
            operator_node.op = '-'
        elif type(ast_bin_op.op) == Mult:
            operator_node.op = '*'
        elif type(ast_bin_op.op) == Div:
            operator_node.op = '/'
        elif type(ast_bin_op.op) == FloorDiv:
            operator_node.op = '//'
        elif type(ast_bin_op.op) == Mod:
            operator_node.op = '%'
        elif type(ast_bin_op.op) == Pow:
            operator_node.op = '**'
        elif type(ast_bin_op.op) == LShift:
            operator_node.op = '<<'
        elif type(ast_bin_op.op) == RShift:
            operator_node.op = '>>'
        elif type(ast_bin_op.op) == BitOr:
            operator_node.op = '|'
        elif type(ast_bin_op.op) == BitAnd:
            operator_node.op = '&'
        elif type(ast_bin_op.op) == MatMult:
            operator_node.op = '@'
        else:
            raise Exception("does not support operator: ", ast_bin_op.op)
        operator_node.left = self.visit(ast_bin_op.left)
        operator_node.right = self.visit(ast_bin_op.right)

        operator_node.add_children(operator_node.left)
        operator_node.add_children(operator_node.right)

        return operator_node
    def visit_Compare(self, ast_compare: Compare):
        operator_node = Operator()
        child_operator_node = Operator()
        left = self.visit(ast_compare.left)
        for index,comparator in enumerate(ast_compare.comparators):
            if index == 0:
                child_operator_node.left = left
                child_operator_node.right = self.visit(comparator)
                child_operator_node.op = self.transform_op(ast_compare.ops[index])
            else:
                parent_operator_node = Operator()
                parent_operator_node.left = child_operator_node
                parent_operator_node.right = self.visit(comparator)
                parent_operator_node.op = self.transform_op(ast_compare.ops[index])
        
        return operator_node
        
    def transform_op(self, compare_op):
        if isinstance(compare_op, ast.Eq):
            return '=='
        if isinstance(compare_op, ast.NotEq):
            return '!='
        if isinstance(compare_op, ast.Lt):
            return '<'
        if isinstance(compare_op, ast.LtE):
            return '<='
        if isinstance(compare_op, ast.Gt):
            return '>'
        if isinstance(compare_op, ast.GtE):
            return '>='
        if isinstance(compare_op, ast.Is):
            return '=='
        if isinstance(compare_op, ast.IsNot):
            return '!='
        if isinstance(compare_op, ast.In):
            return '=='
        if isinstance(compare_op, ast.NotIn):
            return '!='
        else:
            raise Exception("can't support this compare op : ", type(compare_op)) 


    def visit_If(self, ast_if: If):
        if_node = IfNode()
        # coord = coordinate(ast_if.col_offset, ast_if.lineno)
        # self.set_coordinate(if_node, coord)
        # condition
        if_node.condition = self.visit(ast_if.test)

        # convert pyc true statement to list
        if type(ast_if.body) is not list:
            ast_if.body = [ast_if.body]

        self.parent = if_node.true_stmt
        for child in ast_if.body or []:
            child_node = self.visit(child)
            if child_node:
                if type(child_node) is list:
                    if_node.true_stmt.extend(child_node)
                else:
                    if_node.true_stmt.append(child_node)

        # convert pyc false statement to list
        if ast_if.orelse:
            if type(ast_if.orelse) is not list:
                ast_if.orelse = [ast_if.orelse]

            self.parent = if_node.false_stmt
            for child in ast_if.orelse or []:
                child_node = self.visit(child)
                if child_node:
                    if type(child_node) is list:
                        if_node.false_stmt.extend(child_node)
                    else:
                        if_node.false_stmt.append(child_node)
                
        return if_node

    def visit_For(self, ast_for: For):
        for_node = ForNode()

        #init 做出 i = 0
        init_variable = VariableNode()
        init_variable.name = ast_for.target.id
        init_value = ConstantNode()
        init_value.value = 0
        init = AssignNode()
        init.target = init_variable
        init.value = init_value
        # print(init)
        if type(init) is list:
            for_node.init.extend(init)
        else:
            for_node.init.append(init)


        #term 做出 i < n
        term_right = self.for_iter(ast_for.iter)
        term_left = init_variable
        term = Operator()
        term.op = '<'
        term.left = term_left
        term.right = term_right
        for_node.term = term

        #update
        update = AssignNode()
        #i
        update_target = VariableNode()
        update_target.name = ast_for.target.id
        #i+1
        update_value = Operator()
        update_value.left = update_target
        one = ConstantNode()
        one.value = 1
        update_value.right = one
        update_value.op = '+'
        #i = i+1
        update.target = update_target
        update.value = update_value
        if type(update) is list:
            for_node.update.extend(update)
        else:
            for_node.update.append(update)

        for child in ast_for.body:
            child_node = self.visit(child)
            for_node.add_children(child_node)

        return for_node
    
    def for_iter(self, ast_iter):
        if type(ast_iter) == Call:
            if ast_iter.func.id == 'range':
                if len(ast_iter.args) == 1:
                    start = ConstantNode()
                    start.value = 0
                    stop = self.visit(ast_iter.args[0])
                if len(ast_iter.args) == 2:
                    start = self.visit(ast_iter.args[0])
                    stop = self.visit(ast_iter.args[1])

                terminal = Operator()
                terminal.left = stop
                terminal.right = start
                terminal.op = '-'

                if len(ast_iter.args) == 3:
                    step = self(visit(ast_name.args[2]))
                    step_operator_node = Operator()
                    step_operator_node.left = operator_node
                    step_operator_node.right = step
                    step_operator_node.op = '/'
                    terminal = step_operator_node
                return terminal
            else:
                raise Exception("only support function call : range() in for iterator, your function call is: ", ast_node.func.id) 
        else:
            if type(ast_iter) == Name:
                terminal = self.visit(ast_iter)
                return terminal
        raise Exception("can't support this iter type : ", type(ast_node)) 

    def generic_visit(self, node):
        children = []
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        child = self.visit(item)
                        if type(child) is list:
                            children.extend(child)
                        else:
                            children.append(child)

            elif isinstance(value, AST):
                child = self.visit(value)
                if type(child) is list:
                    children.extend(child)
                else:
                    children.append(child)
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