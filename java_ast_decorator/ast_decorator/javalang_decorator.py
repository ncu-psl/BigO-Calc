from javalang.ast import Node
from javalang.tree import CompilationUnit, ForControl, MethodDeclaration, MethodInvocation, Literal, MemberReference, \
    BinaryOperation

from bigo_ast.bigo_ast import BasicNode, CompilationUnitNode, FuncCallNode, FuncDeclNode, ForNode


class AstNodeDecorator(object):

    def __init__(self):

        pass

    def decorate(self, java_node: Node):
        if java_node is None:
            return

        if type(java_node) == Node or not issubclass(java_node.__class__, Node):
            raise Exception("Should init with a subclass of pycparser.c_ast.Node")

        basic_node = BasicNode()

        if java_node.position:
            basic_node.col = java_node.position.column
            basic_node.line_number = java_node.position.line

        return basic_node


class CompilationUnitDecorator(AstNodeDecorator):

    def __init__(self):
        super().__init__()

        pass

    def decorate(self, java_cu: CompilationUnit):
        basic_node = super().decorate(java_cu)

        cu = CompilationUnitNode()
        cu.copy_node_info_from(basic_node)

        return cu


class MethodDeclDecorator(AstNodeDecorator):
    def __init__(self):
        super().__init__()

        pass

    def decorate(self, java_method_decl: MethodDeclaration):
        basic_node = super().decorate(java_method_decl)

        func_decl = FuncDeclNode()
        func_decl.copy_node_info_from(basic_node)

        func_decl.name = java_method_decl.name
        if java_method_decl.parameters:
            for param in java_method_decl.parameters:
                func_decl.parameter.append(param.type.name + ' ' + param.name)

        return func_decl


class MethodInvokeDecorator(AstNodeDecorator):
    def __init__(self):
        super().__init__()

        pass

    def decorate(self, java_method_invoke: MethodInvocation):
        basic_node = super().decorate(java_method_invoke)

        func_call = FuncCallNode()
        func_call.copy_node_info_from(basic_node)
        func_call.name = java_method_invoke.member
        if java_method_invoke.arguments:
            for arg in java_method_invoke.arguments:
                if type(arg) == Literal:
                    func_call.parameter.append(str(arg.value))
                elif type(arg) == MemberReference:
                    func_call.parameter.append(str(arg.member))
                elif type(arg) == BinaryOperation:
                    func_call.parameter.append(str(arg.operandl) + str(arg.operator) + str(arg.operandr))
                else:
                    func_call.parameter.append(str(arg))

        # if java_method_invoke.args:
        #     for param in java_method_invoke.args.exprs:
        #         if isinstance(param, Constant):
        #             func_call.parameter.append(param.value)
        #         elif isinstance(param, ID):
        #             func_call.parameter.append(param.name)

        return func_call


class ForControlDecorator(AstNodeDecorator):
    def __init__(self):
        super().__init__()

        pass

    def decorate(self, java_for: ForControl):
        basic_node = super().decorate(java_for)

        for_node = ForNode()
        for_node.copy_node_info_from(basic_node)

        for_node.variable = str(java_for.init[0].expressionl.member)
        for_node.init = str(java_for.init[0].value.value)
        for_node.term = str(java_for.condition.operandr.member)
        for_node.next = str(java_for.update[0].postfix_operators[0])

        return for_node
