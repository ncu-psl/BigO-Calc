import operator

import sympy
from sympy.core.mul import Mul
from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, IfNode, VariableNode, \
    AssignNode, ArrayNode, ConstantNode, Operator, WhileNode, ClassNode
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from symbol_table.table_manager import table_manager

class BigOCalculator(BigOAstVisitor):

    def __init__(self, root: CompilationUnitNode):
        self.root = root
        self.function_list = []
        self.backward_table_manager = table_manager()
        self.current_class = None
        for func in root.children:
            if type(func) == FuncDeclNode:
                self.function_list.append(func)

        pass

    def calc(self):
        super().visit(self.root)

        pass
    


    def visit_CompilationUnitNode(self, compilation_unit_node: CompilationUnitNode):
        self.backward_table_manager.push_table('compilation')
        print('enter compilation\n')

        tc = 0
        for child in compilation_unit_node.children:
            self.visit(child)
            if (type(child) != FuncDeclNode) and (type(child) != ClassNode):
                print('child type',type(child))
                tc += child.time_complexity
        if tc == 0:
            tc = sympy.Rational(1)
        compilation_unit_node.time_complexity = tc
        print('leave compilation\n')

        self.backward_table_manager.pop_table()

    def visit_ClassNode(self, class_node : ClassNode):
        self.current_class = class_node.name
        for child in class_node.children:
            self.visit(child)
        self.current_class = None

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        if func_decl_node.determine_recursion():
            func_decl_node.time_complexity = sympy.Symbol(func_decl_node.name, integer=True, positive=True)
        else:
            tc = 0
            print('enter funcDec\n')
            self.backward_table_manager.push_table('funcdef')

            for child in func_decl_node.children:
                self.visit(child)
                tc += child.time_complexity
            if tc == 0:
                tc = 1
            func_decl_node.time_complexity = tc
            
            self.backward_table_manager.pop_table()
            print('leave funcDec\n')

        pass

    def visit_FuncCallNode(self, func_call: FuncCallNode):
        target = func_call.name
        for func in self.function_list:
            if target == func.name:
                func_call.time_complexity = sympy.Symbol(func.name, integer=True, positive=True)
                break

        return sympy.Symbol('size('+target+'())', integer=True, positive=True)

    def visit_VariableNode(self, variable_node: VariableNode):
        return sympy.Symbol(variable_node.name, integer=True, positive=True)

    def visit_ArrayNode(self, array_node: ArrayNode):
        tc = 0
        for child in array_node.array:
            self.visit(child)
            tc += child.time_complexity
        array_node.time_complexity = tc 
        return array_node.time_complexity

    def visit_ConstantNode(self, const_node: ConstantNode):
        return sympy.Rational(const_node.value)
        
    def visit_AssignNode(self, assign_node: AssignNode):
        target = assign_node.target
        value = assign_node.value
        self.visit(target)

        value_tc = 0

        self.backward_table_manager.add_symbol(assign_node)

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
        
        if type(left) == sympy.Symbol:
            self.backward_table_manager.current_table.can_replace_varables.append(left.name)
        elif type(right) == sympy.Symbol:
            self.backward_table_manager.current_table.can_replace_varables.append(right.name)
            
        node.time_complexity = node.left.time_complexity + node.right.time_complexity

        if op == '+':
            return operator.add(left, right)
        elif op == '-':
            return operator.sub(left, right)
        elif op == '*':
            return operator.mul(left, right)
        elif op == '/':
            return operator.truediv(left, right)
        elif op == '**':
            return left * 2 ** right

    def visit_IfNode(self, if_node: IfNode):
        self.visit(if_node.condition)

        cond_tc = if_node.condition.time_complexity
        self.backward_table_manager.push_table(scope_type = 'if')

        true_tc = 0
        for child in if_node.true_stmt:
            self.visit(child)
            true_tc += child.time_complexity
        if true_tc == 0:
            true_tc = 1

        if len(if_node.false_stmt) != 0:
            self.backward_table_manager.push_table(scope_type = 'else')

        false_tc = 0
        for child in if_node.false_stmt:
            self.visit(child)
            false_tc += child.time_complexity
        if false_tc == 0:
            false_tc = 1

        if len(if_node.false_stmt) != 0:
            self.backward_table_manager.pop_table()

        self.backward_table_manager.pop_table()
        if_node.time_complexity = cond_tc + sympy.Max(true_tc, false_tc)


        pass

    def visit_ForNode(self, for_node: ForNode):
        print('enter for loop\n')
        if len(for_node.init) != 1:
            raise NotImplementedError("len(for_node.init) != 1")
        if len(for_node.update) != 1:
            raise NotImplementedError("len(for_node.update)")
        self.backward_table_manager.push_table()

        # init
        variable = self.visit(for_node.init[0].target)
        a_1 = self.visit(for_node.init[0].value)

        # term
        term = for_node.term
        
        t_left = self.visit(term.left)      
        t_right = self.visit(term.right)
        
        # update
        tc = 0
        

        for child in for_node.children:
            self.visit(child)
            tc += child.time_complexity
        if tc == 0:
            tc = 1

        if type(term.right) == VariableNode:
            right_rate = self.backward_table_manager.get_symbol_rate(term.right.name)
        if type(term.left) == VariableNode:
            left_rate = self.backward_table_manager.get_symbol_rate(term.left.name)

        update = for_node.update[0]
        op = self.visit(update.value)

        step = 0
        if op.is_Add:
            a_n = t_right
            d = op - variable
            if '*' == left_rate or '/' == right_rate:
                q = 2
                step = sympy.log(a_n, q) + 1
            else:
                step = (a_n - a_1) / d + 1
                
        elif op.is_Mul:
            a_n = t_right
            q = op / variable
            step = sympy.log(a_n, q) + 1
        else:
            raise NotImplementedError('can not handle loop update, op=', op)
        print('type(step)',type(step))

        if step.expand().is_negative:
            raise NotImplementedError('this loop can not analyze.\n')
        self.backward_table_manager.pop_table()
        tc *= step

        for child in for_node.init:
            tc += child.time_complexity
        self.visit(for_node.term)
        tc += for_node.term.time_complexity
        for child in for_node.update:
            tc += child.time_complexity

        for_node.time_complexity = tc
        print('leave for loop\n')
        pass
    

    def visit_WhileNode(self, while_node: WhileNode):
        self.backward_table_manager.push_table()

        cond = while_node.cond

      
        c_left = self.visit(cond.left)
        c_right = self.visit(cond.right)

        tc = 0
        for child in while_node.children:
            self.visit(child)
            tc += child.time_complexity
        if tc == 0:
            tc = 1

        step = 0
        if type(cond.right) == VariableNode:
            right_rate = self.backward_table_manager.get_symbol_rate(cond.right.name)
        if type(cond.left) == VariableNode:
            left_rate = self.backward_table_manager.get_symbol_rate(cond.left.name)


        if cond.op in ['<','<=']:
            a_n = c_right
            a_1 = c_left
            print('an',a_n)
            print('left_rate',left_rate)
            print('right_rate',right_rate)
            if '*' == left_rate or '/' == right_rate:
                q = 2
                step = sympy.log(a_n, q) + 1
                print('type(step)',type(step))

            elif '+' == left_rate or '-' == right_rate:
                d = 1
                step = (a_n) / d + 1
                print('type(step)',type(step))



        elif cond.op in ['>', '>=']:
            a_n = c_left
            a_1 = c_right
            if '/' == left_rate or '*' == right_rate:
                q = 2
                step = sympy.log(a_n / a_1, q) + 1
            elif '-' == left_rate or '+' == right_rate:
                d = 1
                step = (a_n - a_1) / d + 1
        
        else:
            raise NotImplementedError('can not handle loop update, op=', cond.op)
        if step.expand().is_negative:
            raise NotImplementedError('this loop can not analyze.\n', )
        self.backward_table_manager.pop_table()
        while_node.time_complexity = step * tc

        pass