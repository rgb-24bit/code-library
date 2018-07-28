# -*- coding: utf-8 -*-

import functools
from collections import OrderedDict

import yaml
from yaml import Loader, Dumper


def _get_oredered_loader(Loader):
    """Get OrderedLoader."""
    class _OrderedLoader(Loader):
        pass

    def _construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    _OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _construct_mapping)

    return _OrderedLoader


def _get_oredered_dumper(Dumper):
    """ Get OrderedDumper."""
    class _OrderedDumper(Dumper):
        pass

    def _representer_mapping(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    _OrderedDumper.add_representer(OrderedDict, _representer_mapping)

    return _OrderedDumper


OrderedLoader = _get_oredered_loader(Loader)
OrderedDumper = _get_oredered_dumper(Dumper)

load = functools.partial(yaml.load, Loader=OrderedLoader)
load_all = functools.partial(yaml.load_all, Loader=OrderedLoader)

dump = functools.partial(yaml.dump, Dumper=OrderedDumper)
dump_all = functools.partial(yaml.dump_all, Dumper=OrderedDumper)
