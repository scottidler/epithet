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
        for i, arg in enumerate(self.cmdline):
            alias = self.cfg.get(arg)
            if alias:
                cmdline += alias.replace(i)
            else:
                cmdline += [arg]
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
    eprint(f'ns.cmdline={ns.cmdline}')
    epithet = Epithet(CONFIGS, split(ns.cmdline))
    print(*epithet.replace())

if __name__ == '__main__':
    main(sys.argv[1:])
