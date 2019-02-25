import pycparser
from pycparser.c_ast import FileAST


class ASTGenerator(object):
    def __init__(self):
        pass

    def generate(self, filename: str) -> FileAST:
        ast = pycparser.parse_file(filename,
                                   use_cpp=True,
                                   cpp_path='cpp',
                                   cpp_args=r'-Iutils/fake_libc_include')

        return ast
