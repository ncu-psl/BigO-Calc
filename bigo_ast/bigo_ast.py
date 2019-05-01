import json


class BasicNode(object):

    def __init__(self):
        self.time_complexity = 1
        self.__children = []
        self.col = 0
        self.line_number = 0
        self.parent = None
        self.__type = self.__class__.__name__

        pass

    def __iter__(self):
        for child in self.__children:
            yield child

    @property
    def children(self) -> []:
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children

    def add_children(self, children):
        if not children:
            return

        if type(children) is list:
            self.__children.extend(children)
        else:
            self.__children.append(children)

    def add_parent_to_children(self):
        for child in self.__children:
            child.parent = self
            child.add_parent_to_children()
        pass

    def copy_node_info_from(self, basic_node):
        self.time_complexity = basic_node.time_complexity
        self.__children = basic_node.children
        self.col = basic_node.col
        self.line_number = basic_node.line_number
        self.parent = basic_node.parent

        pass

    def to_dict(self):
        d = {'_type': self.__type,
             'time_complexity': self.time_complexity,
             'col': self.col,
             'line_number': self.line_number,
             'parent': None}

        children_list = []
        for child in self.__children:
            children_list.append(child.to_dict())

        d.update({'children': children_list})

        return d

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)


class Bool(BasicNode):

    def __init__(self):
        super().__init__()

        pass


class And(Bool):

    def __init__(self):
        super().__init__()

        pass


class Or(Bool):

    def __init__(self):
        super().__init__()

        pass


class Operator(BasicNode):

    def __init__(self):
        super().__init__()

        self.op = ''
        self.left = BasicNode()
        self.right = BasicNode()

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'left': self.left.to_dict()})
        d.update({'right': self.right.to_dict()})

        return d


class Add(Operator):

    def __init__(self):
        super().__init__()

        pass


class Sub(Operator):

    def __init__(self):
        super().__init__()

        pass


class Mul(Operator):

    def __init__(self):
        super().__init__()

        pass


class Div(Operator):

    def __init__(self):
        super().__init__()

        pass


class CompareOp(BasicNode):

    def __init__(self):
        super().__init__()

        pass


class LT(CompareOp):

    def __init__(self):
        super().__init__()

        pass


class LE(CompareOp):

    def __init__(self):
        super().__init__()

        pass


class GT(CompareOp):

    def __init__(self):
        super().__init__()

        pass


class GE(CompareOp):

    def __init__(self):
        super().__init__()

        pass


class AssignNode(BasicNode):

    def __init__(self):
        super().__init__()
        self.__target = BasicNode()
        self.__value = BasicNode()

        pass

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target
        self.add_children(self.target)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.add_children(self.value)

    def to_dict(self):
        d = super().to_dict()
        d.update({'target': self.target.to_dict()})
        d.update({'value': self.value.to_dict()})

        return d


class VariableNode(BasicNode):

    def __init__(self):
        super().__init__()

        self.name = ''

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'value': self.name})

        return d


class ConstantNode(BasicNode):

    def __init__(self):
        super().__init__()

        self.value = 0

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'value': self.value})

        return d


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

    def to_dict(self):
        d = super().to_dict()
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

    def to_dict(self):
        d = super().to_dict()
        d.update({'name': self.name})
        d.update({'parameter': self.parameter})

        return d


class IfNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.condition = BasicNode()
        self.__true_stmt = []
        self.__false_stmt = []

        pass

    @property
    def true_stmt(self):
        return self.__true_stmt

    @true_stmt.setter
    def true_stmt(self, true_stmt):
        self.__true_stmt = true_stmt

    @property
    def false_stmt(self):
        return self.__false_stmt

    @false_stmt.setter
    def false_stmt(self, false_stmt):
        self.__false_stmt = false_stmt

    def to_dict(self):
        d = super().to_dict()
        d.update({'condition': self.condition.to_dict()})
        d.update({'true': self.true_stmt})
        d.update({'false': self.false_stmt})

        return d


class ForNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.variable = None
        self.init = []
        self.term = []
        self.update = []

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'variable': self.variable})

        init_list = []
        for child in self.init:
            init_list.append(child.to_dict())

        d.update({'init': init_list})

        term_list = []
        for child in self.init:
            term_list.append(child.to_dict())
        d.update({'terminal': term_list})

        update_list = []
        for child in self.init:
            update_list.append(child.to_dict())
        d.update({'update': update_list})

        return d


class WhileNode(BasicNode):
    def __init__(self):
        super().__init__()

        self.term = None

        pass

    def to_dict(self):
        d = super().to_dict()
        d.update({'terminal': self.term})

        return d
