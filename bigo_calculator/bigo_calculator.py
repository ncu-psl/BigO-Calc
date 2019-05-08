import operator

import sympy

from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, IfNode, VariableNode, \
    AssignNode, ConstantNode, Operator
from bigo_ast.bigo_ast_visitor import BigOAstVisitor


class BigOCalculator(BigOAstVisitor):

    def __init__(self, root: CompilationUnitNode):
        self.root = root
        self.function_list = []
        for func in root.children:
            if type(func) == FuncDeclNode:
                self.function_list.append(func)

        pass

    def calc(self):
        super().visit(self.root)

        pass

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        if func_decl_node.determine_recursion():
            func_decl_node.time_complexity = sympy.Symbol(func_decl_node.name)
        else:
            tc = 0
            for child in func_decl_node.children:
                self.visit(child)
                tc += child.time_complexity
            func_decl_node.time_complexity = tc

        pass

    def visit_FuncCallNode(self, func_call: FuncCallNode):
        target = func_call.name
        for func in self.function_list:
            if target == func.name:
                func_call.time_complexity = sympy.Symbol(func.name)
                break

        pass

    def visit_VariableNode(self, variable_node: VariableNode):
        return sympy.Symbol(variable_node.name, integer=True, positive=True)

    def visit_ConstantNode(self, const_node: ConstantNode):
        return sympy.Rational(const_node.value)

    def visit_AssignNode(self, assign_node: AssignNode):
        target = assign_node.target
        value = assign_node.value
        self.visit(target)

        value_tc = 0
        if type(value) is not list:
            self.visit(value)
            value_tc = value.time_complexity
        else:
            for child in value:
                self.visit(child)
                value_tc += child.time_complexity

        assign_node.time_complexity = value_tc

        pass

    def visit_Operator(self, node: Operator):
        op = node.op
        left = self.visit(node.left)
        right = self.visit(node.right)

        node.time_complexity = node.left.time_complexity + node.right.time_complexity

        if op == '+':
            return operator.add(left, right)
        elif op == '-':
            return operator.sub(left, right)
        elif op == '*':
            return operator.mul(left, right)
        elif op == '/':
            return operator.truediv(left, right)
        elif op == '<<':
            return left * 2 ** right
        elif op == '>>':
            return left / (2 ** right)

    def visit_IfNode(self, if_node: IfNode):
        self.visit(if_node.condition)
        cond_tc = if_node.condition.time_complexity

        true_tc = 0
        for child in if_node.true_stmt:
            self.visit(child)
            true_tc += child.time_complexity

        false_tc = 0
        for child in if_node.false_stmt:
            self.visit(child)
            false_tc += child.time_complexity

        if_node.time_complexity = cond_tc + sympy.Max(true_tc, false_tc)

        pass

    def visit_ForNode(self, for_node: ForNode):
        if len(for_node.init) != 1:
            raise NotImplementedError("len(for_node.init) != 1")
        if len(for_node.update) != 1:
            raise NotImplementedError("len(for_node.update)")

        # init
        variable = self.visit(for_node.init[0].target)
        a_1 = self.visit(for_node.init[0].value)

        # term
        term = for_node.term
        t_left = self.visit(term.left)
        t_right = self.visit(term.right)

        if variable == t_left:
            a_n = t_right
        elif variable == t_right:
            a_n = t_left
        else:
            raise NotImplementedError("unknown condition: ", t_left, t_right)

        if term.op == '<' or term.op == '>':
            a_n = a_n - 1

        # update
        update = for_node.update[0]
        op = self.visit(update.value)

        step = 0
        if op.is_Add:
            d = op - variable
            step = (a_n - a_1) / d + 1
        elif op.is_Mul:
            q = op / variable
            step = sympy.log(a_n / a_1, q) + 1

        tc = 0
        for child in for_node.children:
            self.visit(child)
            tc += child.time_complexity
        for_node.time_complexity = step * tc

        pass
