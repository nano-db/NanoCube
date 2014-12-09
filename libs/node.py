
class Node(object):
    def __init__(self):
        super(Node, self).__init__()
        self.proper_children = dict()
        self.shared_child = None
        self.content = None
        self.shared_content = None

    def has_a_single_child(self):
        return len(self.proper_children) == 1

    def has_shared_content(self):
        return self.shared_content is not None

    def has_proper_content(self):
        return self.content is not None

    @staticmethod
    def is_shared_child(node, child):
        return (node.shared_child is not None
                and node.shared_child == child)

    def set_shared_content(self, node):
        self.shared_content = node

    def set_proper_content(self, node):
        self.content = node

    def get_child(self, key):
        return self.proper_children.get(key)

    def add_proper_child(self, key, node):
        self.proper_children[key] = node

    def get_content(self):
        if self.shared_content is not None:
            return self.shared_content
        else:
            return self.content
