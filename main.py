from bigo_calculator.bigo_evaluator import BigOEvaluator
from ast_decorator.java.ast_generator import ASTGenerator
from ast_decorator.java.decorate_visitor import DecorateVisitor


def main():
    # source_file_name = 'examples/FullTest.c'
    # bigo_ast_file_name = 'examples/big-o ast.json'
    source_file_name = 'examples/FullTest.java'
    bigo_ast_file_name = 'examples/big-o ast.json'

    # C frontend
    # ast = ASTGenerator().generate(source_file_name)
    # bigo_ast = DecorateVisitor().visit(ast)

    # Java frontend
    origin_ast = ASTGenerator().generate(source_file_name)
    bigo_ast = DecorateVisitor().visit(origin_ast)

    BigOEvaluator(bigo_ast).eval()

    print(bigo_ast.to_json())

    f = open(bigo_ast_file_name, 'w')
    f.write(bigo_ast.to_json())
    f.close()

    pass


main()
