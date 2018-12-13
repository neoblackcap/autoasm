# -*- coding: utf-8 -*-
import autoasm

ctx = autoasm.Context('testing')
ctx.configure_from_module('autoasm')


@ctx.service('db_name')
def dummy_db():
    return 'testing'


@ctx.inject('db_name')
def get_db_name(db_name):
    return db_name


def test_module_config():
    assert get_db_name() == 'testing'
