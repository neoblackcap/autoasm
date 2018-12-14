# -*- coding: utf-8 -*-
import ast
import importlib
import json
import pathlib

from . import execptions


class Config:

    def to_dict(self):
        """

        :rtype: typing.Mapping
        """
        raise NotImplementedError()


class ModuleConfig(Config):

    def __init__(self, path):
        self._mod = importlib.import_module(path)

    def to_dict(self):
        attrs = [attr for attr in dir(self._mod) if not attr.startswith('_')]
        r = {attr: getattr(self._mod, attr) for attr in attrs}
        return r


class JsonConfig(Config):
    def __init__(self, path):
        self._path = path
        p = pathlib.Path(path)
        if p.exists():
            self._fd = p.open()
        else:
            raise TypeError('json config file is not exists')

    def to_dict(self):

        data = json.load(self._fd)
        values = data['values']

        rv = {}  # return value
        for item in values:
            name = item['name']
            ov = item['value']
            t = item['type']

            try:
                v = self._coerce(ov, t)
            except TypeError:
                _msg = 'parse item with key {key} error'
                msg = _msg.format(key=name)
                raise execptions.ConfigError(msg)
            else:
                rv[name] = v
        return rv

    def _coerce(self, value, kind):
        """

        :param str|int|float|list|dict value:
        :param str kind:
        :return:
        """

        if kind == 'str':
            return str(value)
        elif kind == 'int':
            return int(value)
        elif kind == 'float':
            return float(value)
        elif kind == 'bool':
            return bool(value)
        elif kind == 'list':
            if isinstance(value, list):
                return value
            raise TypeError('value {} is not list'.format(value))
        elif kind == 'dict':
            if isinstance(value, dict):
                return value
            raise TypeError('value {} is not dict'.format(value))
        else:
            raise TypeError('unknown type')




