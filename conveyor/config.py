# -*- coding: utf-8 -*-
import importlib

from conveyor import execptions


class Config:
    pass


class PythonConfig(Config):

    def __init__(self, path):
        self._mod = importlib.import_module(path)

    def __getattribute__(self, key):
        mod = object.__getattribute__(self, '_mod')

        try:
            return getattr(mod, key)
        except AttributeError:
            raise execptions.NoConfig(key)
