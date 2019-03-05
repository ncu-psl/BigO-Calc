from bigo_calculator.bigo_evaluator import BigOEvaluator
from java_ast_decorator.ast_decorator.decorate_visitor import DecorateVisitor
from java_ast_decorator.ast_generator.ast_generator import ASTGenerator


def main():
    # source_file_name = 'c_ast_decorator/examples/FullTest.c'
    # bigo_ast_file_name = 'c_ast_decorator/examples/big-o ast.json'
    source_file_name = 'java_ast_decorator/examples/FullTest.java'
    bigo_ast_file_name = 'java_ast_decorator/examples/big-o ast.json'

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
