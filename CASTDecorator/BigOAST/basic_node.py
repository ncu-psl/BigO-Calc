import json


class BasicNode(object):

    # __slots__ = ["time_complexity", "children", "col", "line_number", "parent", "_type"]

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
