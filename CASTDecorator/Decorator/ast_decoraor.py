from pycparser.c_ast import Node, For, FileAST, FuncDef

from BigOAST.basic_node import BasicNode
from BigOAST.compilation_unit_node import CompilationUnitNode
from BigOAST.func_decl_node import FuncDeclNode


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

    def decorate_func_def(self, func_def: FuncDef):
        func_decl = FuncDeclNode(self.decorate(func_def))

        func_decl.name = func_def.decl.name
        if func_def.decl.type.args:
            param_list = func_def.decl.type.args.params
            for param in param_list:
                func_decl.parameter.append(param.type.type.names[0] + ' ' + param.name)
        return func_decl


class FileAstDecorator2(Decorator):

    def __init__(self):
        super().__init__()
        pass

    def decorate(self, file_ast: FileAST):
        cu = super().decorate(file_ast)
        cu = CompilationUnitNode()
        return cu


class FuncDefDecorator(Decorator):
    def __init__(self):
        super().__init__()
        pass

    def decorate(self, func_def: Node):
        func_decl = super().decorate(func_def)
        func_decl.__class__ = FuncDeclNode
        func_decl.name = func_def.decl.name
        if func_def.decl.type.args:
            param_list = func_def.decl.type.args.params
            for param in param_list:
                func_decl.parameter.append(param.type.type.names[0] + ' ' + param.name)
        return func_decl


class ForDecorator(Decorator):
    def __init__(self):
        super().__init__()
        pass

    def decorate(self, pycparser_for: For):
        for_node = super().decorate(pycparser_for)

        for_node.init = pycparser_for.init.lvalue.name + pycparser_for.init.op + pycparser_for.init.rvalue.value
        for_node.term = pycparser_for.cond.left.name + pycparser_for.cond.op + pycparser_for.cond.right.name
        for_node.next = pycparser_for.next.expr.name + pycparser_for.next.op[1:]
        pass
