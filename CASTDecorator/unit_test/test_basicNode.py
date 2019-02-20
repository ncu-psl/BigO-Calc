import json
from unittest import TestCase

from pycparser.c_ast import Node

from BigOAST.basic_node import BasicNode


class TestBasicNode(TestCase):
    def test___init___with_pycparser_c_ast_Node(self):
        try:
            BasicNode(Node())
            self.fail()
        except Exception:
            pass

    def test___init___coord(self):
        self.fail()
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
            self.assertEqual(child, son[ind])
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
            self.assertEqual(child.parent, root)

    def test_add_parent_to_children_nested(self):
        father = BasicNode()
        son = BasicNode()
        grand_son = BasicNode()

        father.children.append(son)
        son.children.append(grand_son)

        father.add_parent_to_children()

        self.assertEqual(son.parent, father)
        self.assertEqual(grand_son.parent, son)

    def test_to_dect(self):
        basic_node = BasicNode()
        dic = {'_type': 'BasicNode',
               'time_complexity': '',
               'col': 0,
               'line_number': 0,
               'parent': None,
               'children': []}
        self.assertDictEqual(basic_node.to_dect(), dic)

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

        self.assertDictEqual(root.to_dect(), dic)

    def test_to_json(self):
        root = BasicNode()
        self.assertEqual(root.to_json(),
                         json.dumps({'_type': 'BasicNode',
                                     'time_complexity': '',
                                     'col': 0,
                                     'line_number': 0,
                                     'parent': None,
                                     'children': []}, indent=4, sort_keys=True))
