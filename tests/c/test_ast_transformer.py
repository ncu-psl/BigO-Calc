from ast_transformer.c.ast_generator import CASTGenerator
from ast_transformer.c.transform_visitor import CTransformVisitor


def test_ast_generator():
    assert CASTGenerator().generate('examples/FullTest.c')


def test_transform_visitor():
    pyc_ast = CASTGenerator().generate('examples/FullTest.c')
    assert CTransformVisitor().transform(pyc_ast)
