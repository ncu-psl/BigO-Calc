import os

from ast_decorator.c.ast_generator import CASTGenerator
from ast_decorator.c.decorate_visitor import CDecorateVisitor
from ast_decorator.java.ast_generator import JavaASTGenerator
from ast_decorator.java.decorate_visitor import JavaDecorateVisitor
from bigo_calculator.bigo_evaluator import BigOEvaluator


def main():
    source_file_name = 'FullTest.c'
    bigo_ast_file_name = 'big-o ast.json'

    # get language from extension
    language = os.path.splitext(source_file_name)[1][1:].lower()

    # decorate ast
    if language == 'c':
        origin_ast = CASTGenerator().generate(source_file_name)
        bigo_ast = CDecorateVisitor().visit(origin_ast)
    elif language == 'java':
        origin_ast = JavaASTGenerator().generate(source_file_name)
        bigo_ast = JavaDecorateVisitor().visit(origin_ast)
    else:
        raise Exception("Language does not support : " + language)

    # evaluate big o
    BigOEvaluator(bigo_ast).eval()

    # print ast
    for func in bigo_ast.children:
        if func.time_complexity:
            print(f'[{func.name}] = O(' + func.time_complexity + ')')
        else:
            print(f'[{func.name}] = O(1)')

    # print ast to json file
    f = open(bigo_ast_file_name, 'w')
    f.write(bigo_ast.to_json())
    f.close()

    pass


main()
