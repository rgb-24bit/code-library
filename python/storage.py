# -*- coding: utf-8 -*-

"""
Object for saving data.
"""

import threading

from collections import UserDict
from threading import local as threadlocal


class Storage(dict):
    """A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
    """
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'


def storify(mapping):
    """Create a storage object from mapping."""
    return Storage(mapping.items())


def dictify(storage_obj):
    """Create a dict object from storage_obj"""
    return dict(storage_obj.items())


class ThreadedDict(threadlocal):
    """
    Thread local storage.

        >>> d = ThreadedDict()
        >>> d.x = 1
        >>> d.x
        1
        >>> import threading
        >>> def f(): d.x = 2
        ...
        >>> t = threading.Thread(target=f)
        >>> t.start()
        >>> t.join()
        >>> d.x
        1
    """
    _instances = set()

    def __init__(self):
        ThreadedDict._instances.add(self)

    def __del__(self):
        ThreadedDict._instances.remove(self)

    def __hash__(self):
        return id(self)

    @staticmethod
    def clear_all():
        """Clears all ThreadedDict instances."""
        for t in list(ThreadedDict._instances):
            t.clear()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def clear(self):
        self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def pop(self, key, *args):
        return self.__dict__.pop(key, *args)

    def popitem(self):
        return self.__dict__.popitem()

    def setdefault(self, key, default=None):
        return self.__dict__.setdefault(key, default)

    def update(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)

    def __repr__(self):
        return '<ThreadedDict %r>' % self.__dict__

    __str__ = __repr__


class Memoize(object):
    """
    'Memoizes' a function, caching its return values for each input.
    If `expires` is specified, values are recalculated after `expires` seconds.
    If `background` is specified, values are recalculated in a separate thread.

        >>> calls = 0
        >>> def howmanytimeshaveibeencalled():
        ...     global calls
        ...     calls += 1
        ...     return calls
        >>> fastcalls = memoize(howmanytimeshaveibeencalled)
        >>> howmanytimeshaveibeencalled()
        1
        >>> howmanytimeshaveibeencalled()
        2
        >>> fastcalls()
        3
        >>> fastcalls()
        3
        >>> import time
        >>> fastcalls = memoize(howmanytimeshaveibeencalled, .1, background=False)
        >>> fastcalls()
        4
        >>> fastcalls()
        4
        >>> time.sleep(.2)
        >>> fastcalls()
        5
        >>> def slowfunc():
        ...     time.sleep(.1)
        ...     return howmanytimeshaveibeencalled()
        >>> fastcalls = memoize(slowfunc, .2, background=True)
        >>> fastcalls()
        6
        >>> timelimit(.05)(fastcalls)()
        6
        >>> time.sleep(.2)
        >>> timelimit(.05)(fastcalls)()
        6
        >>> timelimit(.05)(fastcalls)()
        6
        >>> time.sleep(.2)
        >>> timelimit(.05)(fastcalls)()
        7
        >>> fastcalls = memoize(slowfunc, None, background=True)
        >>> threading.Thread(target=fastcalls).start()
        >>> time.sleep(.01)
        >>> fastcalls()
        9
    """
    def __init__(self, func, expires=None, background=True): 
        self.func = func
        self.cache = {}
        self.expires = expires
        self.background = background
        self.running = {}

    def __call__(self, *args, **keywords):
        key = (args, tuple(keywords.items()))
        if not self.running.get(key):
            self.running[key] = threading.Lock()

        def update(block=False):
            if self.running[key].acquire(block):
                try:
                    self.cache[key] = (self.func(*args, **keywords), time.time())
                finally:
                    self.running[key].release()

        if key not in self.cache:
            update(block=True)
        elif self.expires and (time.time() - self.cache[key][1]) > self.expires:
            if self.background:
                threading.Thread(target=update).start()
            else:
                update()
        return self.cache[key][0]
