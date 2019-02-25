from pycparser.c_ast import Node, For, FileAST, Constant, ID

from BigOAst.BigOAST import BasicNode, CompilationUnitNode, FuncCallNode, FuncDeclNode, ForNode


class Decorator(object):

    def __init__(self):

        pass

    def decorate(self, node: Node):
        if node is None:
            return

        if type(node) == Node or not issubclass(node.__class__, Node):
            raise Exception("Should init with a subclass of pycparser.c_ast.Node")

        basic_node = BasicNode()

        if node.coord:
            basic_node.col = node.coord.column
            basic_node.line_number = node.coord.line

        return basic_node


class FileAstDecorator(Decorator):

    def __init__(self):
        super().__init__()

        pass

    def decorate(self, file_ast: FileAST):
        basic_node = super().decorate(file_ast)

        cu = CompilationUnitNode()
        cu.set_info(basic_node)

        return cu


class FuncDefDecorator(Decorator):
    def __init__(self):
        super().__init__()

        pass

    def decorate(self, func_def: Node):
        basic_node = super().decorate(func_def)

        func_decl = FuncDeclNode()
        func_decl.set_info(basic_node)
        func_decl.name = func_def.decl.name
        if func_def.decl.type.args:
            param_list = func_def.decl.type.args.params
            for param in param_list:
                func_decl.parameter.append(param.type.type.names[0] + ' ' + param.name)

        return func_decl


class FuncCallDecorator(Decorator):
    def __init__(self):
        super().__init__()

        pass

    def decorate(self, py_func_call: Node):
        basic_node = super().decorate(py_func_call)

        func_call = FuncCallNode()
        func_call.set_info(basic_node)
        func_call.name = py_func_call.name.name
        if py_func_call.args:
            for param in py_func_call.args.exprs:
                if isinstance(param, Constant):
                    func_call.parameter.append(param.value)
                elif isinstance(param, ID):
                    func_call.parameter.append(param.name)

        return func_call


class ForDecorator(Decorator):
    def __init__(self):
        super().__init__()

        pass

    def decorate(self, pyc_for: For):
        basic_node = super().decorate(pyc_for)

        for_node = ForNode()
        for_node.set_info(basic_node)
        for_node.init = pyc_for.init.lvalue.name + pyc_for.init.op + pyc_for.init.rvalue.value
        for_node.term = pyc_for.cond.left.name + pyc_for.cond.op + pyc_for.cond.right.name
        for_node.next = pyc_for.next.expr.name + pyc_for.next.op[1:]

        return for_node
