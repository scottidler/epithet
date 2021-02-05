#!/usr/bin/env python3
import os
import re
import sys

from shlex import split
from ruamel import yaml
from leatherman.repr import __repr__

CONFIGS = [
    '~/config/epithet/epithet.yml',
    '~/.epithet.yml',
    './epithet.yml',
]

class NoConfigFoundError(Exception):
    def __init__(self, configs):
        msg = f'no config found error: configs={configs}'
        super().__init__(msg)

class ConfigNotLoadedError(Exception):
    def __init__(self, config):
        msg = f'config not loaded error: config={config}'
        super().__init__(msg)

class Alias:
    def __init__(self, name, value, expand=False, space=False, first=False):
        self.name = name
        self.value = value
        self.expand = expand
        self.space = space
        self.first = first

    @property
    def args(self):
        return split(self.value)

    def replace(self, pos):
        if not self.first or (self.first and pos==0):
            return split(self.value)
        return [self.name]

    __repr__ = __repr__

def find(configs):
    for config in configs:
        if os.path.isfile(config):
            return config
    raise NoConfigFoundError(configs)

def load(config):
    cfg = {}
    yml = yaml.safe_load(open(config))
    if yml:
        for key, value in yml.items():
            cfg[key] = Alias(key, value) if isinstance(value, str) else Alias(key, **value)
    if cfg:
        return cfg
    raise ConfigNotLoadedError(config)

class Epithet:
    def __init__(self, configs, args):
        self.config = find(configs)
        self.cfg = load(self.config)
        self.args = args

    __repr__ = __repr__

    def replace(self):
        args = []
        for i, arg in enumerate(self.args):
            alias = self.cfg.get(arg)
            if alias:
                args += alias.replace(i)
            else:
                args += [arg]
#            if alias and (not alias.first or (alias.first and i==0)):
#                args += alias.args
#                continue
#            args += [arg]
        return args

def main(args):
    epithet = Epithet(CONFIGS, args)
    print(*epithet.replace())

if __name__ == '__main__':
    main(sys.argv[1:])
