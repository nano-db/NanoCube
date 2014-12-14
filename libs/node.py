import sys


class Node(object):
    def __init__(self):
        super(Node, self).__init__()
        self.proper_children = dict()
        self.shared_children = dict()
        self.proper_content = None
        self.shared_content = None

    @property
    def children(self):
        """Return dict of proper and shared children

        :rtype : dict
        """
        return dict(self.proper_children.items() + self.shared_children.items())

    @property
    def content(self):
        """Get the content of the current node

        :rtype : Node
        """
        if self.proper_content is not None:
            return self.proper_content
        else:
            return self.shared_content

    @property
    def has_a_single_child(self):
        """Return true if the node as a single child

        :rtype : bool
        """
        return len(self.children) == 1

    @property
    def has_shared_content(self):
        """Return True if the content is shared

        :rtype: bool
        """
        return self.shared_content is not None

    @property
    def has_proper_content(self):
        """Return True if the content is proper

        :rtype:bool
        """
        return self.proper_content is not None

    @staticmethod
    def is_shared_child(node, child):
        """Return true is node as child as a shared child

        :param node:Node Parent node to test
        :param child:Node Child node to test
        :rtype:bool
        """
        return child in node.shared_children.values()

    def set_shared_content(self, node):
        """Set a node as shared content

        :param node:Node
        """
        self.proper_content = None
        self.shared_content = node

    def set_proper_content(self, node):
        """Set a node as proper content

        :param node:Node
        """
        self.shared_content = None
        self.proper_content = node

    def get_child(self, key):
        """Return the node linked by the key
        If no node is found return None

        :type key:str
        :rtype:Node
        """
        if self.proper_children.get(key) is not None:
            return self.proper_children.get(key)
        else:
            return self.shared_children.get(key)

    def add_proper_child(self, key, node):
        """Add the node as proper child link by key
        If there is already a shared child, this child is deleted

        :type node:Node
        """
        if self.shared_children.get(key) is not None:
            del self.shared_children[key]
        self.proper_children[key] = node

    def add_shared_child(self, key, node):
        self.shared_children[key] = node

    def copy(self):
        """Execute a shallow copy of the node

        :rtype:Node
        """
        node_copy = Node()
        node_copy.set_shared_content(self.content)
        for key in self.children:
            node_copy.add_shared_child(key, self.children[key])
        return node_copy

    def __sizeof__(self):
        size = sys.getsizeof(self.proper_children)
        size += sys.getsizeof(self.proper_content)
        for key in self.shared_children.keys():
            size += sys.getsizeof(key)
        return size
