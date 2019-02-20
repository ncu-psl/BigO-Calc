from src.ast_generator import ASTGenerator
from src.decorate_visitor import Decorator


def main():
    ast = ASTGenerator().generate('test/FullTest.c')

    bigo_ast = Decorator().decorate(ast)

    print(bigo_ast.to_json())

    f = open("test/big-o ast.json", "w")
    f.write(bigo_ast.to_json())
    f.close()

    pass


main()
