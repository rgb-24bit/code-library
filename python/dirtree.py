# -*- coding: utf-8 -*-

"""
Simple directory tree structure.
"""

from pathlib import Path


class DirectoryTreeNode(object):
    """Directory tree node object.

    Args:
        path: The path of the file represented by the current node.
        depth: The depth of the current node in the directory tree.
        parent: The parent node of the current node.
    """
    def __init__(self, path, depth, parent):
        self.path = Path(path)
        self.depth = depth
        self.parent = parent

        self.name = self.path.name
        self.child = []

    def add_child_node(self, child_node_path):
        child_node = DirectoryTreeNode(child_node_path, self.depth + 1, self)

        found_node = self._find_child_node(child_node)
        if not found_node:
            self.child.append(child_node)
            return child_node

        return found_node


    def _find_child_node(self, child_node):
        for _child_node in self.child:
            if _child_node.path == child_node.path:
                return _child_node
        return None

    def __repr__(self):
        return self.path.__repr__()


def make_root_node(path):
    return DirectoryTreeNode(path, -1, None)


def generate_directory_tree(root):
    for child in root.path.iterdir():
        child_node = root.add_child_node(child)

        if child_node.path.is_dir():
            generate_directory_tree(child_node)


if __name__ == '__main__':
    pass
