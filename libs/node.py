import sys
import re


class Node(object):
    def __init__(self, id):
        super(Node, self).__init__()
        self.proper_children = dict()
        self.shared_children = dict()
        self.proper_content = None
        self.shared_content = None
        self.id = id

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

    def copy(self, cube):
        """Execute a shallow copy of the node

        :rtype:Node
        """
        node_copy = Node(cube)
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

    def dump(self):
        ret = u"{}: ".format(self.id)
        if len(self.proper_children) > 0:
            ref = {key: self.proper_children[key].id for key in self.proper_children}
            ret += u"pch: {} ".format(str(ref))
        if len(self.shared_children) > 0:
            ref = {key: self.shared_children[key].id for key in self.shared_children}
            ret += u"sch: {} ".format(str(ref))

        if self.has_proper_content:
            ret += u"pco: {} ".format(self.proper_content.id)
        else:
            ret += u"sco: {} ".format(self.shared_content.id)

        return ret + "\n"

    @classmethod
    def load(cls, line, nodes):
        pattern = "(\d+): (?:pch: ([^p|s]+))?(?:sch: ([^p|s]+))?(?:(?:pco: (.+))|(?:sco: (.+)))"
        m = re.search(pattern, line)

        id = int(m.group(1))
        node = Node(id)

        if m.group(2) is not None:
            node.proper_children = eval(m.group(2))
            for key in node.proper_children:
                val = node.proper_children[key]
                node.proper_children[key] = nodes[val]
        if m.group(3) is not None:
            node.shared_children = eval(m.group(3))
            for key in node.shared_children:
                val = node.shared_children[key]
                node.shared_children[key] = nodes[val]

        if m.group(4) is not None:
            node.proper_content = nodes[int(m.group(4))]
        else:
            node.shared_content= nodes[int(m.group(5))]

        return node