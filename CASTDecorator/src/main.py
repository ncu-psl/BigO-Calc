from src.ast_generator import ASTGenerator
from src.pycparser_ast_visitor import PycparserAstVisitor


def main():
    ast = ASTGenerator().generate('examples/FullTest.c')

    bigo_ast = PycparserAstVisitor().visit(ast)

    print(bigo_ast.to_json())

    f = open("examples/big-o ast.json", "w")
    f.write(bigo_ast.to_json())
    f.close()

    pass


main()
