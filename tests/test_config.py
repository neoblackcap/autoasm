# -*- coding: utf-8 -*-
import pathlib

import autoasm

cfg_path = pathlib.Path(__file__).parent / 'config.json'

ctx = autoasm.Context('testing')
ctx.configure_from_module('tests.config')
ctx.configure_from_json(cfg_path.absolute())


@ctx.service('db_name')
@ctx.inject('db')
def dummy_db(db):
    return db


@ctx.service('username')
@ctx.inject('name')
def dummy_name(name):
    return name


@ctx.inject('db_name')
def get_db_name(db_name):
    return db_name


@ctx.inject('username')
def get_dummy_name(username):
    return username


def test_module_config():
    assert get_db_name() == 'testing'


def test_json_config():
    assert get_dummy_name() == 'tester'
