# -*- coding: utf-8 -*-

"""
A simple language for getting members in a regular JSON object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Introduction:
    + The basic operators are `[` and `.`
    + You can get the key value of the json object by `.`, like `.key`
    + You can also pass the `[` get json array to specify the index of the object,
      like `[index`
    + Indexes can also be represented in regular form, like `[0]`
    + The first member of the statement can be omitted `[` and `.`

Example:
    >>> dt = dict(key=[dict(key=dict(key=2))])
    >>> dt
    {'key': [{'key': {'key': 2}}]}
    >>> dt['key'][0]['key']['key']
    2
    >>> jsonquery(dt, 'key[0].key.key')
    2

:copyright: (c) 2018 - 2019 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import collections
import re


Token = collections.namedtuple('Token', ['type', 'value'])

TOKENS = (
    r'(?P<KEY>\w+)',
    r'(?P<INDEX>\d+)',
    r'(?P<DOT>\.)',
    r'(?P<LSPAREN>\[)',
    r'(?P<RSPAREN>\])'
)

_mathcer = re.compile('|'.join(TOKENS))


def generate_tokens(string):
    scanner = _mathcer.scanner(string)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())


def jsonquery(jsonobj, query_string):
    prev_token = Token('NULL', None)
    for token in generate_tokens(query_string):
        if token.type == 'KEY':
            if prev_token.type == 'LSPAREN':
                jsonobj = jsonobj[int(token.value)]
            else:
                jsonobj = jsonobj[token.value]
        elif token.type == 'INDEX':
            jsonobj = jsonobj[int(token.value)]
        prev_token = token
    return jsonobj
