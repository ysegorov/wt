# -*- coding: utf-8 -*-

import os
import logging

from collections import OrderedDict
from string import Template

import yaml

from .decorators import reloadable


logger = logging.getLogger('wt.base')


@reloadable('(re)loading nested configuration...')
def load_yaml(filename):
    with open(filename, encoding='utf-8') as f:
        data = list(yaml.load_all(f))
    return data[0] if len(data) == 1 else data


class ObjectDict(dict):

    def __getattr__(self, name, default=None):
        return self.process_value(self.get(name, default))

    def __setattr__(self, name, value):
        self[name] = value

    def process_value(self, v):
        if isinstance(v, str):
            v = Template(v).safe_substitute(**os.environ)
            v = self.load_file(v)
        return v

    def load_file(self, v):
        if isinstance(v, str) and v[:6] == '{file}':
            workdir = self.get('_workdir', '')
            v = load_yaml(os.path.join(workdir, v[6:]))
            if isinstance(v, dict):
                v = ObjectDict(v)
        return v

    def path(self, path, dflt=None):
        parts = path.split('.')
        src = self
        for idx, p in enumerate(parts[:-1]):
            src = src.get(p)
            src = self.process_value(src)
            if src is None:
                break
            if not isinstance(src, dict):
                msg = ('Expecting %s instance to have value for "%s"'
                       ' but "%s" found at "%s" instead of nested dict'
                       % (type(self).__name__,
                          path,
                          str(src),
                          '.'.join(parts[:idx + 1])))
                raise ValueError(msg)
        v = src and src.get(parts[-1], dflt)
        if isinstance(v, dict):
            v = ObjectDict(v)
        return self.process_value(dflt if v is None else v)


class OrderedObjectDict(OrderedDict, ObjectDict):
    pass


class Config(ObjectDict):
    pass


class Content(ObjectDict):
    content_dirname = 'content'
    data_dirname = None

    @classmethod
    def from_dict(cls, workdir, data):
        p = cls(data)
        if p.src and not os.path.isabs(p.src):
            p.src = os.path.join(workdir,
                                 cls.content_dirname,
                                 cls.data_dirname or '',
                                 p.src)
        return p

    @property
    def text(self):
        t = ''
        if self.src and os.path.isfile(self.src):
            with open(self.src, 'rt', encoding='utf-8') as f:
                t = f.read()
        else:
            logger.warn('  ! missing content file "%s"', self.src)
        return t


class Page(Content):
    data_dirname = 'pages'


class Post(Content):
    data_dirname = 'posts'
