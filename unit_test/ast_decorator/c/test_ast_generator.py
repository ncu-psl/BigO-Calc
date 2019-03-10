import os
from unittest import TestCase

from pycparser.c_ast import FileAST

from ast_decorator.c.ast_generator import ASTGenerator


class TestASTGenerator(TestCase):

    def test_generate(self):
        # change working directory to ast_decorator/c/
        dirname = os.path.basename(os.getcwd())
        while dirname != 'ABOAT':
            os.chdir('..')
            dirname = os.path.basename(os.getcwd())
        os.chdir('ast_decorator/c/')

        self.assertEqual(FileAST, type(ASTGenerator().generate("../../examples/FullTest.c")))

    def test_generate_file_not_found(self):
        # change working directory to ast_decorator/c/
        dirname = os.path.basename(os.getcwd())
        while dirname != 'ABOAT':
            os.chdir('..')
            dirname = os.path.basename(os.getcwd())
        os.chdir('ast_decorator/c/')
        try:
            ASTGenerator().generate("something does not exist")
            self.fail()
        except FileNotFoundError:
            pass
