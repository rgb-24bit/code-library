# -*- coding: utf-8 -*-

import os
import pathlib


class FileVisitor(object):
    """Accessing objects that process files during file tree traversal."""

    def pre_visit_directory(self, dirname):
        """Method called before accessing the directory.

        Args:
            dirname: The pathlib.Path object of the directory to be accessed.
        """
        pass

    def post_visit_directory(self, dirname):
        """Method called after accessing the directory.

        Args:
            dirname: The pathlib.Path object of the directory to be accessed.
        """
        pass

    def visit_file(self, filename):
        """Method called when accessing a file.

        Args:
            filename: The pathlib.Path object of the file to be accessed.
        """

    def error_handler(self, error):
        """Method called when an exception occurs during traversal.

        Args:
            error: An instance of the exception that occurred.
        """
        pass


class FileTreeWalker(object):
    """File tree traversal object.

    Args:
        path: The directory to be traversed.
        visitor: Object that implements the FileVisitor interface.
        followlinks: Whether to traverse the symbolic link under the directory,
            the default is False.
    """
    def __init__(self, path, visitor, followlinks=False):
        self.visitor = visitor
        self.walker = os.walk(path, onerror=visitor.error_handler,
                              followlinks=followlinks)

    def walk(self):
        """Traversing the file tree."""
        try:
            dirpath, dirnames, filenames = next(self.walker)

            for dirname in dirnames:
                dirname = pathlib.Path(dirname)
                self.visitor.pre_visit_directory(dirname)
                self.walk()
                self.visitor.post_visit_directory(dirname)

            for filename in filenames:
                self.visitor.visit_file(pathlib.Path(filename))
        except StopIteration:
            pass


if __name__ == '__main__':
    pass
