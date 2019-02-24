from BigOAST.basic_node import BasicNode
from BigOAST.compilation_unit_node import CompilationUnitNode


class BigOASTVisitor(object):
    _method_cache = None

    def __init__(self, root: CompilationUnitNode):
        self.root = root

        pass

    def visit(self, node: BasicNode):
        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, current_node: BasicNode):
        for node in current_node:
            self.visit(node)
