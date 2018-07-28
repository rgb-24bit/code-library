# -*- coding: utf-8 -*-

"""
Traverse collection.
"""

class TraverseCollection(object):
    __slots__ = ('serializer',)

    key = None

    def __init__(self, serializer):
        self.serializer = serializer

    def check(self, value):
        raise NotImplementedError

    def traverse(self, value):
        raise NotImplementedError


class TraverseDict(TraverseCollection):
    __slots__ = ()

    key = ' d'

    def check(self, value):
        return isinstance(value, dict)

    def traverse(self, value):
        return dict(((k, self.serializer.traverse(v)) for k, v in value.items()))


class TraverseList(TraverseCollection):
    __slots__ = ()

    key = ' l'

    def check(self, value):
        return isinstance(value, list)

    def traverse(self, value):
        return [self.serializer.traverse(item) for item in value]


class TraverseTuple(TraverseCollection):
    __slots__ = ()

    key = ' t'

    def check(self, value):
        return isinstance(value, tuple)

    def traverse(self, value):
        return tuple([self.serializer.traverse(item) for item in value])


class TraverseCollectionSerializer(object):
    __slots__ = ('traverses', 'order')

    default_traverses = [
        TraverseDict, TraverseList, TraverseTuple
    ]

    def __init__(self):
        self.order = list()

        for cls in self.default_traverses:
            self.register(cls)

    def register(self, traverse_class, force=False, index=None):
        traverse = traverse_class(self)

        if index is None:
            self.order.append(traverse)
        else:
            self.order.insert(index, traverse)

    def traverse(self, value):
        for traverse in self.order:
            if traverse.check(value):
                return traverse.traverse(value)

        return value
