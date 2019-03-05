import os

import pycparser
from pycparser.c_ast import FileAST


class ASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str) -> FileAST:
        if not os.path.isfile(filename):
            raise FileNotFoundError
        ast = pycparser.parse_file(filename,
                                   use_cpp=True,
                                   cpp_path='cpp',
                                   cpp_args=r'-Ic_ast_decorator/utils/fake_libc_include')

        return ast
