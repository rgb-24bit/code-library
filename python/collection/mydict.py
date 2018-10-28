# -*- coding: utf-8 -*-

class NestedDict(dict):
    """Automated nested dictionary.

    >>> nd = NestedDict()
    >>> nd['a']['b']['c'] = 1
    >>> nd
    {'a': {'b': {'c': 1}}}
    """
    def __getitem__(self, key):
        return self.setdefault(key, self.__class__())
