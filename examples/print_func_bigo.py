import json
import os
import sys

from ast_decorator.c.ast_generator import CASTGenerator
from ast_decorator.c.decorate_visitor import CDecorateVisitor
from ast_decorator.java.ast_generator import JavaASTGenerator
from ast_decorator.java.decorate_visitor import JavaDecorateVisitor
from bigo_calculator.bigo_evaluator import BigOEvaluator

bigo_ast_file_name = 'function time complexity.json'

def main():
    if len(sys.argv) == 0:
        raise EnvironmentError("not enough argument")
    elif len(sys.argv) > 3:
        raise EnvironmentError("too many arguments")

    source_file_name = sys.argv[1]

    # default get programming language by extension
    language = os.path.splitext(source_file_name)[1][1:].lower()
    if len(sys.argv) == 2:
        language = sys.argv[2]

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
