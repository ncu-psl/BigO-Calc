import json
import os
import sys

import sympy

from ast_decorator.c.ast_generator import CASTGenerator
from ast_decorator.c.transform_visitor import CTransformVisitor
from ast_decorator.java.ast_generator import JavaASTGenerator
from ast_decorator.java.transform_visitor import JavaTransformVisitor
from bigo_ast.bigo_ast import FuncDeclNode
from bigo_calculator.bigo_calculator import BigOCalculator
from bigo_calculator.bigo_simplify import BigOSimplify


def main():
    if len(sys.argv) == 0:
        raise EnvironmentError("not enough argument")
    elif len(sys.argv) > 3:
        raise EnvironmentError("too many arguments")

    source_file_name = sys.argv[1]

    # default get programming language by extension
    language = os.path.splitext(source_file_name)[1][1:].lower()
    if len(sys.argv) == 3:
        language = sys.argv[2].lower()

    # transform ast
    if language == 'c':
        origin_ast = CASTGenerator().generate(source_file_name)
        bigo_ast = CTransformVisitor().transform(origin_ast)
    elif language == 'java':
        origin_ast = JavaASTGenerator().generate(source_file_name)
        bigo_ast = JavaTransformVisitor().transform(origin_ast)
    else:
        raise Exception("Language does not support : " + language)

    # evaluate big o
    BigOCalculator(bigo_ast).calc()
    BigOSimplify(bigo_ast).simplify()

    func_bigo_dict = {}
    for func in bigo_ast.children:
        if type(func) != FuncDeclNode:
            continue

        complexity = func.time_complexity
        if not complexity:
            func.time_complexity = sympy.Rational(1)
            complexity = sympy.Rational(1)
        elif func.recursive:
            complexity = 'is a recursive function call'
        else:
            if type(complexity) is sympy.Order:
                complexity = str(complexity)
            else:
                complexity = 'O(' + str(complexity) + ')'
        func_bigo_dict.update({func.name: complexity})

    json_str = json.dumps(func_bigo_dict, indent=4)

    # print function Big-O
    print(json_str)

    return json_str


main()
