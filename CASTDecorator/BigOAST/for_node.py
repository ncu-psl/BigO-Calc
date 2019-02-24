from BigOAST.basic_node import BasicNode


class ForNode(BasicNode):
    def __init__(self):
        super().__init__()

        # self.init = ' '.join(str(x) for x in for_node.init or [])
        # self.term = ' '.join(str(x) for x in for_node.cond or [])
        # self.next = ' '.join(str(x) for x in for_node.next or [])

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
