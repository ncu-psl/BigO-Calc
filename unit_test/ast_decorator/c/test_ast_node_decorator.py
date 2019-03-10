from unittest import TestCase

from pycparser.c_ast import Node, FileAST, ID

from ast_decorator.c.ast_node_decorator import Decorator, FileAstDecorator
from bigo_ast.bigo_ast import BasicNode


class TestDecorator(TestCase):
    def test_decorate_pycparser_node(self):
        try:
            Decorator().decorate(Node())
            self.fail()
        except Exception as e:
            if str(e) != 'Should init with a subclass of pycparser.c_ast.Node':
                self.fail()

    def test_decorate_other_node(self):
        try:
            a = 0
            type(Decorator().decorate(a))
            self.fail()
        except Exception as e:
            if str(e) != 'Should init with a subclass of pycparser.c_ast.Node':
                self.fail()

    def test_decorate_pycparser_sub_node(self):
        fake_ext = object
        self.assertEqual(BasicNode, type(Decorator().decorate(FileAST(ext=fake_ext))))

    def test_decorate_have_coord(self):
        class Coord:
            colum = 0
            file = ''
            line = 0

        fake_coord = Coord()
        fake_coord.column = 1
        fake_coord.file = 'unittest'
        fake_coord.line = 2

        ast = ID(name='', coord=fake_coord)
        basic_node = Decorator().decorate(ast)
        self.assertEqual(1, basic_node.col)
        self.assertEqual(2, basic_node.line_number)

    pass


class TestFileAstDecorator(TestCase):
    def test_decorate(self):
        fake_ext = 0
        file_ast = FileAST(fake_ext)
        self.assertIsNotNone(FileAstDecorator().decorate(file_ast))


class TestFuncDefDecorator(TestCase):
    def test_decorate(self):
        self.fail()


class TestFuncCallDecorator(TestCase):
    def test_decorate(self):
        self.fail()


class TestForDecorator(TestCase):
    def test_decorate(self):
        self.fail()
