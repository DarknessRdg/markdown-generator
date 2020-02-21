class BaseObject:
    """
    Class to store function data
    Attributes:
        doc: function's docstring
    """
    def __init__(self):
        self.doc = ''


class Tree:
    """
    Tree to store an objects children
    Attributes:
        current: current objects
        children: list of current's children objects
    """

    def __init__(self, current):
        self.current = current
        self.children = []

    def __len__(self):
        return len(self.current)
