# -*- coding: utf-8 -*-

import os
import pathlib


class FileTreeWalker(object):
    """File tree traversal object.

    Args:
        path: The directory to be traversed.
        followlinks: Whether to traverse the symbolic link under the directory,
            the default is False.
    """
    def __init__(self, path, followlinks=False):
        self.walker = os.walk(path, onerror=self.error_handler,
                              followlinks=followlinks)

    def error_handler(self):
        pass

    def pre_visit_directory(self, dirname):
        pass

    def post_visit_directory(self, dirname):
        pass

    def visit_file(self, filename):
        pass

    def walk(self):
        """Traversing the file tree."""
        try:
            dirpath, dirnames, filenames = next(self.walker)

            for dirname in dirnames:
                dirname = pathlib.Path(dirname)
                self.pre_visit_directory(dirname)
                self.walk()
                self.post_visit_directory(dirname)

            for filename in filenames:
                self.visit_file(pathlib.Path(filename))

        except StopIteration:
            pass
