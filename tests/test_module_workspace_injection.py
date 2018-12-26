# -*- coding: utf-8 -*-
import importlib

import autoasm
from .base import ws

ctx = autoasm.Context('testing')


@ws.inject('foo')
def get_foo(foo):
    return foo


def load_module(name):
    importlib.import_module(name)


load_module('tests.dummy')
ctx.workspace(ws)


def test_inject():
    assert get_foo() == 'bar'
