from src.ast_generator.ast_generator import ASTGenerator
from src.ast_decorator.decorate_visitor import DecorateVisitor


def main():
    ast = ASTGenerator().generate('examples/FullTest.c')

    bigo_ast = DecorateVisitor().visit(ast)

    print(bigo_ast.to_json())

    f = open("examples/big-o ast.json", "w")
    f.write(bigo_ast.to_json())
    f.close()

    pass


main()
