from ast import Module, FunctionDef, Call, Starred, Assign, AnnAssign, Attribute, AugAssign,\
    BinOp, BoolOp, And, Or, Add, Sub, Mult, FloorDiv, Pow, Mod, Div, Num, Name, If, For, NodeVisitor, iter_fields, AST, Compare, List, Tuple
import ast


class print_ast_visitor(NodeVisitor):
    def __init__(self):
        self.parent = None
        self.name = '#'
        pass

    def print_node(self, root):
        self.visit(root)
        return self.name

    def visit_Call(self, ast_call: Call):
        self.visit(ast_call.func)
        self.name += '('
        if ast_call.args:
            for arg in ast_call.args:
                self.visit(arg)
                self.name += ','
            self.name = self.name[:-1]
        self.name+=')'
    
    def visit_Name(self, ast_name: Name):
        self.name += ast_name.id

    def visit_Attribute(self, ast_attribute: Attribute):
        self.visit(ast_attribute.value)
        self.name += '.' + ast_attribute.attr
        
    def visit_Num(self, ast_num):
        self.name += str(ast_num.n)
    
    def visit_BinOp(self, ast_op):
        self.visit(ast_op.left)

        if type(ast_op.op) == Add:
            op = '+'
        elif type(ast_op.op) == Sub:
            op = '-'
        elif type(ast_op.op) == Mult:
            op = '*'
        elif type(ast_op.op) == Div:
            op = '/'
        elif type(ast_op.op) == FloorDiv:
            op = '//'
        elif type(ast_op.op) == Mod:
            op = '%'
        elif type(ast_op.op) == Pow:
            op = '**'
        elif type(ast_op.op) == LShift:
            op = '<<'
        elif type(ast_op.op) == RShift:
            op = '>>'
        elif type(ast_op.op) == BitOr:
            op = '|'
        elif type(ast_op.op) == BitAnd:
            op = '&'
        elif type(ast_op.op) == MatMult:
            op = '@'
        self.name += op
        self.visit(ast_op.right)