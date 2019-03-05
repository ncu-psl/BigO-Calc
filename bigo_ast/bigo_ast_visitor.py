from bigo_ast.bigo_ast import BasicNode


class BigOAstVisitor(object):
    _method_cache = None
    root = BasicNode()

    def visit(self, node: BasicNode = None):
        if node is None:
            node = self.root

        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, node: BasicNode):
        for c in node.children:
            self.visit(c)
