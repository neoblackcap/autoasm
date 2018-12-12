# -*- coding: utf-8 -*-
import importlib
import typing

from . import execptions


class Config:

    def to_dict(self) -> typing.Mapping:
        raise NotImplementedError()


class PythonFileConfig(Config):

    def __init__(self, path):
        self._mod = importlib.import_module(path)

    def __getattribute__(self, key):
        mod = object.__getattribute__(self, '_mod')

        try:
            return getattr(mod, key)
        except AttributeError:
            raise execptions.NoConfig(key)

    def to_dict(self):
        attrs = [attr for attr in dir(self._mod) if not attr.startswith('_')]
        r = {attr: getattr(attr, self._mod) for attr in attrs}
        return r


class JsonConfig(Config):
    pass


class ObjectConfig(Config):
    pass
