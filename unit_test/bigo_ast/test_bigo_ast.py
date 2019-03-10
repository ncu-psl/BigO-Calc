import json
from unittest import TestCase

from bigo_ast.bigo_ast import BasicNode, CompilationUnitNode, FuncDeclNode, FuncCallNode, ForNode


class TestBasicNode(TestCase):
    def test___init___(self):
        basic_node = BasicNode()
        self.assertEqual('', basic_node.time_complexity)
        self.assertEqual([], basic_node.children)
        self.assertEqual(0, basic_node.col)
        self.assertEqual(0, basic_node.line_number)
        self.assertEqual(None, basic_node.parent)
        self.assertEqual(type(basic_node).__name__, basic_node._type)

        pass

    def test__iter__does_not_have_children(self):
        root = BasicNode()
        for child in root:
            self.fail()

        pass

    def test__iter__have_children(self):
        root = BasicNode()
        son = [BasicNode(), BasicNode()]
        root.children.extend(son)

        ind = 0
        for child in root:
            self.assertEqual(son[ind], child)
            ind = ind + 1

        pass

    def test_add_parent_to_children_null(self):
        root = BasicNode()

        root.add_parent_to_children()
        self.assertIsNotNone(root.children)

    def test_add_parent_to_children(self):
        root = BasicNode()
        root.children.extend([BasicNode(), BasicNode(), BasicNode()])

        root.add_parent_to_children()

        for child in root.children:
            self.assertEqual(root, child.parent)

    def test_add_parent_to_children_nested(self):
        father = BasicNode()
        son = BasicNode()
        grand_son = BasicNode()

        father.children.append(son)
        son.children.append(grand_son)

        father.add_parent_to_children()

        self.assertEqual(father, son.parent)
        self.assertEqual(son, grand_son.parent)

    def test_copy_node_info_from(self):
        root = BasicNode()
        son = BasicNode()
        basic_node = BasicNode()
        basic_node.time_complexity = 'O(N)'
        basic_node.col = 1000
        basic_node.line_number = 1000
        basic_node.parent = root
        basic_node.children = son

        new_node = BasicNode()
        new_node.copy_node_info_from(basic_node)

        self.assertEqual(basic_node.time_complexity, new_node.time_complexity)
        self.assertEqual(basic_node.col, new_node.col)
        self.assertEqual(basic_node.line_number, new_node.line_number)
        self.assertEqual(basic_node.parent, new_node.parent)
        self.assertEqual(basic_node.children, new_node.children)

        pass

    def test_to_dect(self):
        basic_node = BasicNode()
        dic = {'_type': 'BasicNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': []}
        self.assertDictEqual(dic, basic_node.to_dect())

    def test_to_dect_children(self):
        dic = {'_type': 'BasicNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': [{'_type': 'BasicNode',
                             'time_complexity': '',
                             'col': 0,
                             'line_number': 0,
                             'parent': None,
                             'children': []}]}

        root = BasicNode()
        child = BasicNode()
        root.children.append(child)

        self.assertDictEqual(dic, root.to_dect())

    def test_to_json(self):
        root = BasicNode()
        self.assertEqual(json.dumps({'_type': 'BasicNode',
                                     'time_complexity': '',
                                     'col': 0,
                                     'line_number': 0,
                                     'parent': None,
                                     'children': []}, indent=4, sort_keys=True)
                         , root.to_json())


class TestCompilationUnitNode(TestCase):
    def test___init___(self):
        cu = CompilationUnitNode()
        self.assertEqual('', cu.time_complexity)
        self.assertEqual([], cu.children)
        self.assertEqual(0, cu.col)
        self.assertEqual(0, cu.line_number)
        self.assertEqual(None, cu.parent)
        self.assertEqual(type(cu).__name__, cu._type)

        pass


class TestFuncDeclNode(TestCase):
    def test__init__(self):
        func_decl = FuncDeclNode()
        self.assertEqual('', func_decl.time_complexity)
        self.assertEqual([], func_decl.children)
        self.assertEqual(0, func_decl.col)
        self.assertEqual(0, func_decl.line_number)
        self.assertEqual(None, func_decl.parent)
        self.assertEqual(type(func_decl).__name__, func_decl._type)

        self.assertEqual(False, func_decl.recursive)
        self.assertEqual('', func_decl.name)
        self.assertEqual([], func_decl.parameter)

    def test_determine_recursion_grandson_call(self):
        call_func1 = FuncCallNode()
        call_func1.name = 'func1'

        for_node = ForNode()
        for_node.children.append(call_func1)

        func1_decl = FuncDeclNode()
        func1_decl.name = 'func1'
        func1_decl.children.append(for_node)
        self.assertTrue(func1_decl.determine_recursion())

    def test_determine_recursion_does_not_have_children(self):
        func_decl = FuncDeclNode()
        self.assertFalse(func_decl.determine_recursion())

    def test_determine_recursion_call_itself(self):
        call_func1 = FuncCallNode()
        call_func1.name = 'func1'

        func1_decl = FuncDeclNode()
        func1_decl.name = 'func1'
        func1_decl.children.append(call_func1)
        self.assertTrue(func1_decl.determine_recursion())

    def test_determine_recursion_does_not_call_itself(self):
        call_func2 = FuncCallNode()
        call_func2.name = 'func2'

        func1_decl = FuncDeclNode()
        func1_decl.name = 'func1'
        func1_decl.children.append(call_func2)
        self.assertFalse(func1_decl.determine_recursion())

    def test_to_dect(self):
        dic = {'_type': 'FuncDeclNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': [],

               'recursive': False,
               'name': '',
               'parameter': []}

        self.assertDictEqual(dic, FuncDeclNode().to_dect())

    def test_to_dect_children(self):
        dic = {'_type': 'FuncDeclNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': [{'_type': 'BasicNode',
                             'time_complexity': '',
                             'col': 0,
                             'line_number': 0,
                             'parent': None,
                             'children': []}],

               'recursive': False,
               'name': '',
               'parameter': []}

        func_decl = FuncDeclNode()
        child = BasicNode()
        func_decl.children.append(child)

        self.assertDictEqual(dic, func_decl.to_dect())


class TestFuncCallNode(TestCase):
    def test__init__(self):
        func_call = FuncCallNode()
        self.assertEqual('', func_call.time_complexity)
        self.assertEqual([], func_call.children)
        self.assertEqual(0, func_call.col)
        self.assertEqual(0, func_call.line_number)
        self.assertEqual(None, func_call.parent)
        self.assertEqual(type(func_call).__name__, func_call._type)

        self.assertEqual('', func_call.name)
        self.assertEqual([], func_call.parameter)

    def test_to_dect(self):
        dic = {'_type': 'FuncCallNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': [],

               'name': '',
               'parameter': []}

        func_call = FuncCallNode()

        self.assertDictEqual(dic, func_call.to_dect())


class TestForNode(TestCase):
    def test__init__(self):
        for_node = ForNode()
        self.assertEqual('', for_node.time_complexity)
        self.assertEqual([], for_node.children)
        self.assertEqual(0, for_node.col)
        self.assertEqual(0, for_node.line_number)
        self.assertEqual(None, for_node.parent)
        self.assertEqual(type(for_node).__name__, for_node._type)

        self.assertEqual(None, for_node.variable)
        self.assertEqual(None, for_node.init)
        self.assertEqual(None, for_node.term)
        self.assertEqual(None, for_node.next)

    def test_to_dect(self):
        dic = {'_type': 'ForNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': [],

               'init': None,
               'terminal': None,
               'update': None}

        self.assertDictEqual(dic, ForNode().to_dect())

    def test_to_dect_children(self):
        dic = {'_type': 'ForNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': [{'_type': 'BasicNode',
                             'time_complexity': '',
                             'col': 0,
                             'line_number': 0,
                             'parent': None,
                             'children': []}],

               'init': None,
               'terminal': None,
               'update': None}

        for_node = ForNode()
        child = BasicNode()
        for_node.children.append(child)

        self.assertDictEqual(dic, for_node.to_dect())
