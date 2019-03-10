from unittest import TestCase

from pycparser.c_ast import Node, FileAST, ID

from ast_decorator.c.bigo_ast_node_factory import CBigOAstNodeFactory, CCompilationUnitNodeFactory
from bigo_ast.bigo_ast import BasicNode


class TestBigOAstNodeFactory(TestCase):
    def test_create_with_pycparser_node(self):
        try:
            CBigOAstNodeFactory().create(Node())
            self.fail()
        except Exception as e:
            if str(e) != 'Should init with a subclass of pycparser.c_ast.Node':
                self.fail()

    def test_create_with_other_node(self):
        try:
            a = 0
            type(CBigOAstNodeFactory().create(a))
            self.fail()
        except Exception as e:
            if str(e) != 'Should init with a subclass of pycparser.c_ast.Node':
                self.fail()

    def test_create_with_pycparser_sub_node(self):
        fake_ext = object
        self.assertEqual(BasicNode, type(CBigOAstNodeFactory().create(FileAST(ext=fake_ext))))

    def test_create_with_node_have_coord(self):
        class Coord:
            colum = 0
            file = ''
            line = 0

        fake_coord = Coord()
        fake_coord.column = 1
        fake_coord.file = 'unittest'
        fake_coord.line = 2

        ast = ID(name='', coord=fake_coord)
        basic_node = CBigOAstNodeFactory().create(ast)
        self.assertEqual(1, basic_node.col)
        self.assertEqual(2, basic_node.line_number)

    pass


class TestCompilationUnitNodeFactory(TestCase):
    def test_create(self):
        fake_ext = 0
        file_ast = FileAST(fake_ext)
        self.assertIsNotNone(CCompilationUnitNodeFactory().create(file_ast))


class TestFuncDeclNodeFactory(TestCase):
    def test_create(self):
        self.fail()


class TestFuncCallNodeFactory(TestCase):
    def test_create(self):
        self.fail()


class ForNodeFactory(TestCase):
    def test_create(self):
        self.fail()
