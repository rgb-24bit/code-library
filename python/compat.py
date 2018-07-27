# -*- coding: utf-8 -*-

"""
Python2 and Python3 compatible code collection.
"""

import sys


PY2 = sys.version_info[0] == 2


if not PY2:
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())

    is_iter = lambda x: x and hasattr(x, '__next__')

    from io import StringIO

else:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()

    is_iter = lambda x: x and hasattr(x, 'next')

    from cStringIO import StringIO


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    class metaclass(type):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})
