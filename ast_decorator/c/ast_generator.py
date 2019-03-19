import os

import pycparser
from pycparser.c_ast import FileAST


class CASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str) -> FileAST:
        if not os.path.isfile(filename):
            raise FileNotFoundError

        current_dir = os.path.abspath(os.path.dirname(__file__))
        fake_libc_include_path = os.path.join(current_dir, 'pycparser/utils/fake_libc_include')

        ast = pycparser.parse_file(filename,
                                   use_cpp=True,
                                   cpp_path='cpp',
                                   cpp_args='-I' + fake_libc_include_path)

        return ast
