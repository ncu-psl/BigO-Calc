import json
import os
import sys

from ast_decorator.c.ast_generator import CASTGenerator
from ast_decorator.c.decorate_visitor import CDecorateVisitor
from ast_decorator.java.ast_generator import JavaASTGenerator
from ast_decorator.java.decorate_visitor import JavaDecorateVisitor
from bigo_calculator.bigo_evaluator import BigOEvaluator


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

    func_bigo_dict = {}
    for func in bigo_ast.children:
        if not func.time_complexity:
            func.time_complexity = '1'
        func_bigo_dict.update({func.name: 'O(' + func.time_complexity + ')'})

    json_str = json.dumps(func_bigo_dict, indent=4)

    # print function Big-O
    print(json_str)

    return json_str


main()
