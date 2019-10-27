# -*- coding: utf-8 -*-

class Condition(object):
    def __init__(self, obj=None, predicate=None):
        if obj is not None:
            if callable(predicate):
                self.o = obj
                self.p = predicate
            else:
                self.o = obj
                self.p = lambda x: x
        else:
            self.o = True
            self.p = lambda x: x
        self.t = True

    def __bool__(self):
        return self.t and self.p(self.o)


class RangeValue(object):
    def __init__(self):
        self.t = True
        self.v = None


def prange(iterable):
    value = RangeValue()
    for v in iterable:
        value.v = v
        yield value
        if not value.t:
            break


for i in prange(100):
    for j in prange(100):
        for k in prange(100):
            i.t = j.t = k.t = False
