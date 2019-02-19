from BigOAST.compilation_unit_node import CompilationUnitNode
from BigOAST.func_call_node import FuncCallNode
from BigOAST.func_decl_node import FuncDeclNode
from src.ast_generator import ASTGenerator
from src.decorate_visitor import Decorator


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


def main():
    ast = ASTGenerator().generate('test/FullTest.c')

    bigo_ast = Decorator().decorate(ast)

    print(bigo_ast.toJSON())

    f = open("test/big-o ast.json", "w")
    f.write(bigo_ast.toJSON())
    f.close()

    pass


main()
