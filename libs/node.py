
class Node(object):
    def __init__(self):
        super(Node, self).__init__()
        self.proper_childrens = dict()
        self.shared_child = None
        self.content = None
        self.shared_content = None

    def has_a_single_child(self):
        return len(self.proper_childrens) == 1

    def has_shared_content(self):
        return self.shared_content is not None

    def has_proper_content(self):
        return self.content is not None

    def is_shared_child(node, child):
        return (node.shared_child is not None
                and node.shared_child == child)

    def set_shared_content(self, node):
        self.shared_content = node
