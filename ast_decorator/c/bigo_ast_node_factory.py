from pycparser.c_ast import Node, For, FileAST, Constant, ID, If

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

    def create(self, file_ast: FileAST):
        basic_node = super().create(file_ast)

        cu = CompilationUnitNode()
        cu.copy_node_info_from(basic_node)

        return cu


class CFuncDeclNodeFactory(CBigOAstNodeFactory):
    def __init__(self):
        super().__init__()

        pass

    def create(self, func_def: Node):
        basic_node = super().create(func_def)

        func_decl = FuncDeclNode()
        func_decl.copy_node_info_from(basic_node)
        func_decl.name = func_def.decl.name
        if func_def.decl.type.args:
            param_list = func_def.decl.type.args.params
            for param in param_list:
                func_decl.parameter.append(param.type.type.names[0] + ' ' + param.name)

        return func_decl


class CFuncCallNodeFactory(CBigOAstNodeFactory):
    def __init__(self):
        super().__init__()

        pass

    def create(self, py_func_call: Node):
        basic_node = super().create(py_func_call)

        func_call = FuncCallNode()
        func_call.copy_node_info_from(basic_node)
        func_call.name = py_func_call.name.name
        if py_func_call.args:
            for param in py_func_call.args.exprs:
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
        for_node.init = pyc_for.init.rvalue.value
        for_node.term = pyc_for.cond.right.name
        for_node.update = pyc_for.next.op[1:]

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
