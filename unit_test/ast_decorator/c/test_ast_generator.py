import os
from unittest import TestCase

from pycparser.c_ast import FileAST

from ast_decorator.c.ast_generator import CASTGenerator


class TestCASTGenerator(TestCase):

    def test_generate(self):
        # change working directory to project root: ABOAT/
        dirname = os.path.basename(os.getcwd())
        while dirname != 'ABOAT':
            os.chdir('..')
            dirname = os.path.basename(os.getcwd())

        self.assertEqual(FileAST, type(CASTGenerator().generate("examples/FullTest.c")))

    def test_generate_file_not_found(self):
        try:
            CASTGenerator().generate("something does not exist")
            self.fail()
        except FileNotFoundError:
            pass
