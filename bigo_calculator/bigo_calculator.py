import operator

import sympy

from bigo_ast.bigo_ast import FuncDeclNode, ForNode, FuncCallNode, CompilationUnitNode, IfNode, VariableNode, \
    AssignNode, ConstantNode, Operator
from bigo_ast.bigo_ast_visitor import BigOAstVisitor
from symbol_table.table_manager import table_manager, symbol_table, symbol

class BigOCalculator(BigOAstVisitor):

    def __init__(self, root: CompilationUnitNode):
        self.root = root
        self.function_list = []
        self.table_manager = table_manager()
        for func in root.children:
            if type(func) == FuncDeclNode:
                self.function_list.append(func)

        pass

    def calc(self):
        super().visit(self.root)

        pass
    
    def visit_CompilationUnitNode(self, compilation_unit_node: CompilationUnitNode):
        self.table_manager.add_table()
        for child in compilation_unit_node.children:
            self.visit(child)
        self.table_manager.pop_table()

    def visit_FuncDeclNode(self, func_decl_node: FuncDeclNode):
        if func_decl_node.determine_recursion():
            func_decl_node.time_complexity = sympy.Symbol(func_decl_node.name, integer=True, positive=True)
        else:
            tc = 0
            print('enter funcDec')
            self.table_manager.add_table()
            for child in func_decl_node.children:
                self.visit(child)
                tc += child.time_complexity
            if tc == 0:
                tc = 1
            func_decl_node.time_complexity = tc
            
            print(self.table_manager.print_current_table())
            self.table_manager.pop_table()
            print('leave funcDec\n')

        pass

    def visit_FuncCallNode(self, func_call: FuncCallNode):
        target = func_call.name
        for func in self.function_list:
            if target == func.name:
                func_call.time_complexity = sympy.Symbol(func.name, integer=True, positive=True)
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
        
        if type(target) == VariableNode:
            if type(value) == ConstantNode:
#                 print('assign -> var,const')
                self.table_manager.add_symbol(str(target.name), str(value.value))
#                 print(self.table_manager.print_current_table())
            elif type(value) == VariableNode:
#                 print('assign -> var,var')
                self.table_manager.add_symbol(str(target.name), str(value.name))
#                 print(self.table_manager.print_current_table())

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
            self.table_manager.current_table.can_replace_varables.append(left)
        elif type(right) == sympy.Symbol:
            self.table_manager.current_table.can_replace_varables.append(right)
            
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
            print('enter true cond')
            self.table_manager.add_table()
            self.visit(child)
            true_tc += child.time_complexity
            print(self.table_manager.print_current_table())
            self.table_manager.pop_table()
            print('leave true cond\n')
        if true_tc == 0:
            true_tc = 1

        false_tc = 0
        for child in if_node.false_stmt:
            print('enter false cond')
            self.table_manager.add_table()
            self.visit(child)
            false_tc += child.time_complexity
            print(self.table_manager.print_current_table())
            self.table_manager.pop_table()
            print('leave false cond\n')
        if false_tc == 0:
            false_tc = 1

        if_node.time_complexity = cond_tc + sympy.Max(true_tc, false_tc)

        pass

    def visit_ForNode(self, for_node: ForNode):
        if len(for_node.init) != 1:
            raise NotImplementedError("len(for_node.init) != 1")
        if len(for_node.update) != 1:
            raise NotImplementedError("len(for_node.update)")
        self.table_manager.add_table()
       
        # init
        variable = self.visit(for_node.init[0].target)
        a_1 = self.visit(for_node.init[0].value)

        # term
        term = for_node.term
        
        t_left = self.visit(term.left)
        #紀錄可能可以替換的symbol
        if type(t_left) == sympy.Symbol:
            self.table_manager.current_table.can_replace_varables.append(t_left)
            
        t_right = self.visit(term.right)
        #紀錄可能可以替換的symbol
        if type(t_right) == sympy.Symbol:
            self.table_manager.current_table.can_replace_varables.append(t_right)
        
        if variable == t_left:
            a_n = t_right
            if term.op == '<':
                a_n = a_n - 1
            elif term.op == '>':
                a_n = a_n + 1
        elif variable == t_right:
            a_n = t_left
            if term.op == '<':
                a_n = a_n + 1
            elif term.op == '>':
                a_n = a_n - 1
        else:
            raise NotImplementedError("unknown condition: ", t_left, t_right)

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
        else:
            raise NotImplementedError('can not handle loop update, op=', op)

        if step.expand().is_negative:
            raise NotImplementedError('this loop can not analyze.\n', )

        tc = 0
        for child in for_node.children:
            self.visit(child)
            tc += child.time_complexity
        if tc == 0:
            tc = 1
        for_node.time_complexity = step * tc

        #replace symbol
        for symbol in self.table_manager.current_table.can_replace_varables:
#             print('symbol.name : ',symbol.name)
            replace_symbol = self.table_manager.get_symbol_value(symbol.name)
#             print('replace_symbol : ',replace_symbol)
            if replace_symbol != None:
#                 print('replace')
                for_node.time_complexity = for_node.time_complexity.subs(symbol, sympy.Symbol(replace_symbol, integer=True, positive=True))
#             print('for_node.time_complexity :',for_node.time_complexity)
#             print('\n')
        
#         print('for_node_tc',for_node.time_complexity)
        self.table_manager.pop_table()

        pass
