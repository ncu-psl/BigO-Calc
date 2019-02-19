from BigOAST.compilation_unit_node import CompilationUnitNode
from BigOAST.func_call_node import FuncCallNode
from BigOAST.func_decl_node import FuncDeclNode
from src.decorate_visitor import Decorator
from src.ast_generator import ASTGenerator


def set_parent(cu: CompilationUnitNode):
    que = [cu, ]
    while que:
        node = que.pop(0)
        for child in node.children:
            child.parent = node
            que.append(child)

    pass


def clean_parent(cu: CompilationUnitNode):
    que = [cu, ]
    while que:
        node = que.pop(0)
        for child in node.children:
            child.parent = None
            que.append(child)

    pass


def check_recursion(cu: CompilationUnitNode):
    set_parent(bigo_ast)

    que = [cu, ]

    while que:
        node = que.pop(0)
        if isinstance(node, FuncCallNode):
            parent = node.parent
            while parent:
                if isinstance(parent, FuncDeclNode):
                    if node.name == parent.name:
                        node.is_recursion_call = True
                        parent.is_recursion_func = True
                        break
                parent = parent.parent
        for child in node.children:
            que.append(child)

    clean_parent(bigo_ast)

    pass


if __name__ == "__main__":
    ast = ASTGenerator().generate('test/FullTest.c')

    bigo_ast = Decorator().decorate(ast)

    check_recursion(bigo_ast)

    print(bigo_ast.toJSON())

pass
