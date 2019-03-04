import json

from pycparser.c_ast import If


class BasicNode(object):

    def __init__(self):
        self.time_complexity = ''
        self.children = []
        self.col = 0
        self.line_number = 0
        self.parent = None
        self._type = self.__class__.__name__

        pass

    def __iter__(self):
        for child in self.children:
            yield child

    def add_parent_to_children(self):
        for child in self.children:
            child.parent = self
            child.add_parent_to_children()
        pass

    def copy_node_info_from(self, basic_node):
        self.time_complexity = basic_node.time_complexity
        self.children = basic_node.children
        self.col = basic_node.col
        self.line_number = basic_node.line_number
        self.parent = basic_node.parent

        pass

    def to_dect(self):
        d = {'_type': self._type,
             'time_complexity': self.time_complexity,
             'col': self.col,
             'line_number': self.line_number,
             'parent': None}

        children_list = []
        for child in self.children:
            children_list.append(child.to_dect())

        d.update({'children': children_list})

        return d

    def to_json(self):
        return json.dumps(self.to_dect(), indent=4, sort_keys=True)


class CompilationUnitNode(BasicNode):

    def __init__(self):
        super().__init__()

        pass


class FuncDeclNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.recursive = False
        self.name = ''
        self.parameter = []

        pass

    def determine_recursion(self):
        que = [self]

        while que:
            node = que.pop(0)
            if isinstance(node, FuncCallNode):
                if node.name == self.name:
                    self.recursive = True
                    break
            for child in node.children:
                que.append(child)

        return self.recursive

    def to_dect(self):
        d = super().to_dect()
        d.update({'recursive': self.recursive})
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d


class FuncCallNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.name = ''
        self.parameter = []

        pass

    def to_dect(self):
        d = super().to_dect()
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d


class IfNode(BasicNode):
    def __init__(self, if_node: If = None):
        super().__init__(if_node)

        self.condition = ''

        if if_node is None:
            return

        self.condition = ' '.join(str(x) for x in if_node.cond or [])

        pass

    def to_dect(self):
        d = super().to_dect()
        d.update({'condition': self.condition})

        return d


class ForNode(BasicNode):
    def __init__(self):
        super().__init__()

        # self.init = ' '.join(str(x) for x in for_node.init or [])
        # self.term = ' '.join(str(x) for x in for_node.cond or [])
        # self.next = ' '.join(str(x) for x in for_node.next or [])

        self.variable = None
        self.init = None
        self.term = None
        self.next = None

        # self.children = ' '.join(str(x) for x in for_node.stmt.block_items or [])

        pass

    def to_dect(self):
        d = super().to_dect()
        d.update({'init': self.init})
        d.update({'terminal': self.term})
        d.update({'update': self.next})

        return d
