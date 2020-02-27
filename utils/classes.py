import contextlib


class BaseObject:
    """
    Class to store class or function data
    Attributes:
        doc: current object's docstring
        name: objects name
        children: list of other objects that are children of current object
    """
    def __init__(self, name, parent, indent):
        self.doc = ''
        self.name = name
        self.children = []
        self.parent = parent
        self.indent = indent

    def __str__(self):
        return self.name

    def get_md_title(self):
        if self.indent == 0:
            return self.name
        else:
            parent_name = self.parent.get_md_title()
            with contextlib.suppress(ValueError):
                parent_name = parent_name[:parent_name.index('(')]

            return parent_name + '.' + self.name
