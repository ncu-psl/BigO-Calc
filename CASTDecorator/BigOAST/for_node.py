from pycparser.c_ast import For

from BigOAST.basic_node import BasicNode


class ForNode(BasicNode):
    def __init__(self, for_node: For = None):
        super().__init__(for_node)

        # self.init = ' '.join(str(x) for x in for_node.init or [])
        # self.term = ' '.join(str(x) for x in for_node.cond or [])
        # self.next = ' '.join(str(x) for x in for_node.next or [])

        self.init = None
        self.term = None
        self.next = None

        if for_node is None:
            return

        self.init = for_node.init.lvalue.name + for_node.init.op + for_node.init.rvalue.value
        self.term = for_node.cond.left.name + for_node.cond.op + for_node.cond.right.name
        self.next = for_node.next.expr.name + for_node.next.op[1:]

        # self.children = ' '.join(str(x) for x in for_node.stmt.block_items or [])

        pass

    def to_dect(self):
        d = super().to_dect()
        d.update({'init': self.init})
        d.update({'terminal': self.term})
        d.update({'update': self.next})

        return d
