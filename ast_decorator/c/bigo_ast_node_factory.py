from pycparser.c_ast import Node, For, FileAST, Constant, ID, If, ArrayRef, Assignment

from bigo_ast.bigo_ast import BasicNode, CompilationUnitNode, FuncCallNode, FuncDeclNode, ForNode, IfNode


class CBigOAstNodeFactory(object):

    def __init__(self):

        pass

    def create(self, node: Node):

        if type(node) == Node or not issubclass(node.__class__, Node):
            raise Exception("Should init with a subclass of pycparser.c_ast.Node")

        basic_node = BasicNode()

        if node.coord:
            basic_node.col = node.coord.column
            basic_node.line_number = node.coord.line

        return basic_node


class CCompilationUnitNodeFactory(CBigOAstNodeFactory):

    def __init__(self):
        super().__init__()

        pass

    def create(self, pyc_file_ast: FileAST):
        basic_node = super().create(pyc_file_ast)

        cu = CompilationUnitNode()
        cu.copy_node_info_from(basic_node)

        return cu


class CFuncDeclNodeFactory(CBigOAstNodeFactory):
    def __init__(self):
        super().__init__()

        pass

    def create(self, pyc_func_def: Node):
        basic_node = super().create(pyc_func_def)

        func_decl = FuncDeclNode()
        func_decl.copy_node_info_from(basic_node)
        func_decl.name = pyc_func_def.decl.name
        if pyc_func_def.decl.type.args:
            param_list = pyc_func_def.decl.type.args.params
            for param in param_list:
                func_decl.parameter.append(param.type.type.names[0] + ' ' + param.name)

        return func_decl


class CFuncCallNodeFactory(CBigOAstNodeFactory):
    def __init__(self):
        super().__init__()

        pass

    def create(self, pyc_func_call: Node):
        basic_node = super().create(pyc_func_call)

        func_call = FuncCallNode()
        func_call.copy_node_info_from(basic_node)
        func_call.name = pyc_func_call.name.name
        if pyc_func_call.args:
            for param in pyc_func_call.args.exprs:
                if isinstance(param, Constant):
                    func_call.parameter.append(param.value)
                elif isinstance(param, ID):
                    func_call.parameter.append(param.name)

        return func_call


class CForNodeFactory(CBigOAstNodeFactory):
    def __init__(self):
        super().__init__()

        pass

    def create(self, pyc_for: For):
        basic_node = super().create(pyc_for)

        for_node = ForNode()
        for_node.copy_node_info_from(basic_node)

        for_node.variable = pyc_for.init.lvalue.name
        rvalue = pyc_for.init.rvalue
        if hasattr(rvalue, "value"):
            for_node.init = rvalue.value
        elif type(rvalue) == ArrayRef:
            for_node.term = rvalue.name.name + '[' + rvalue.subscript.name + ']'
        elif hasattr(rvalue, "name"):
            for_node.init = rvalue.name

        right = pyc_for.cond.right
        if hasattr(right, "value"):
            for_node.term = right.value
        elif type(right) == ArrayRef:
            for_node.term = right.name.name + '[' + right.subscript.name + ']'
        elif hasattr(right, "name"):
            for_node.term = right.name

        pyc_next = pyc_for.next
        op = pyc_next.op
        if type(pyc_next) == Assignment:
            if pyc_next.lvalue.name == pyc_next.rvalue.left.name:
                if pyc_next.rvalue.op == '*':
                    if pyc_next.rvalue.right.value == '2':
                        for_node.update = '*2'
                elif pyc_next.rvalue.op == '/':
                    if pyc_next.rvalue.right.value == '2':
                        for_node.update = '/2'
        elif op[0] == 'p':
            for_node.update = pyc_for.next.op[1:]
        else:
            for_node.update = op
        return for_node


class CIfNodeFactory(CBigOAstNodeFactory):
    def __init__(self):
        super().__init__()

        pass

    def create(self, pyc_if: If):
        basic_node = super().create(pyc_if)

        if_node = IfNode()
        if_node.copy_node_info_from(basic_node)

        return if_node
