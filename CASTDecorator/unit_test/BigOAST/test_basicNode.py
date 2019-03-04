import json
from unittest import TestCase

from BigOAST.BigOAST import BasicNode


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
