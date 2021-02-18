#!/usr/bin/env python3
import os
import re
import sys
sys.dont_write_bytecode = True

from shlex import split
from ruamel import yaml
from leatherman.repr import __repr__

from argparse import ArgumentParser

DIR = os.path.abspath(os.path.dirname(__file__))
CWD = os.path.abspath(os.getcwd())
REL = os.path.relpath(DIR, CWD)

CONFIGS = [
    '~/config/epithet/epithet.yml',
    '~/.epithet.yml',
    f'{REL}/epithet.yml',
]

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class NoConfigFoundError(Exception):
    def __init__(self, configs):
        msg = f'no config found error: configs={configs}'
        super().__init__(msg)

class ConfigNotLoadedError(Exception):
    def __init__(self, config):
        msg = f'config not loaded error: config={config}'
        super().__init__(msg)

pattern = '\$[1-9]'
regex = re.compile(pattern)
def get_args(value):
    matches = regex.findall(value)
    return sorted(set(matches))

class Alias:
    def __init__(self, name, value, expand=False, space=False, first=False):
        self.name = name
        self.value = value
        self.expand = expand
        self.space = space
        self.first = first
        self.args = get_args(value)

    def replace(self, index, rem):
        if not self.first or (self.first and index==0):
            value = self.value
            if self.args:
                if len(rem) >= len(self.args):
                    index += len(self.args)
                    for var, val in zip(self.args, rem):
                        value = value.replace(var, val)
                    return index, split(value)
                else:
                    return index, [self.name]
            return index, split(value)
        return index, [self.name]

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
    def __init__(self, configs, cmdline):
        self.config = find([
            os.path.expanduser(config)
            for config
            in configs
        ])
        self.cfg = load(self.config)
        self.cmdline = cmdline

    __repr__ = __repr__

    def replace(self):
        cmdline = []
        i = 0
        while i < len(self.cmdline):
            arg = self.cmdline[i]
            rem = self.cmdline[i+1:]
            alias = self.cfg.get(arg)
            if alias:
                i, replacement = alias.replace(i, rem)
                cmdline += replacement
            else:
                cmdline += [arg]
            i += 1
        return cmdline

def main(args):
    parser = ArgumentParser()
    parser.add_argument(
        '-c', '--configs',
        default=CONFIGS,
        nargs='+',
        help='default=%(default)s; set the defaults configs to check',
    )
    parser.add_argument(
        'cmdline',
        help='the cmdline',
    )
    ns = parser.parse_args(args)
    epithet = Epithet(CONFIGS, split(ns.cmdline))
    print(*epithet.replace())

if __name__ == '__main__':
    main(sys.argv[1:])
