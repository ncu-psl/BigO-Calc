import os

import pycparser
from pycparser.c_ast import FileAST


class CASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str) -> FileAST:
        if not os.path.isfile(filename):
            raise FileNotFoundError
        ast = pycparser.parse_file(filename,
                                   use_cpp=True,
                                   cpp_path='cpp',
                                   cpp_args=r'-Iast_decorator/c/pycparser/utils/fake_libc_include')

        return ast
