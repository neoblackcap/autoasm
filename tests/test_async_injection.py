# -*- coding: utf-8 -*-

import pytest

import autoasm

ctx = autoasm.Context('testing')
ws = autoasm.Workspace('testing')
ws2 = autoasm.Workspace('testing')


@ctx.service('movie_finder')
class MovieFinder:
    def list_real_names(self):
        return ['Peter', 'Tony']


class MovieLister:
    @ctx.inject('movie_finder')
    def __init__(self, movie_finder: MovieFinder):
        self._movie_finder = movie_finder

    def list_real_names(self):
        return self._movie_finder.list_real_names()


@ctx.async_service('movie_lister')
async def movie_lister_factory():
    return MovieLister()


@ctx.inject('movie_lister')
async def get_names(movie_lister):
    return movie_lister.list_real_names()


@ctx.inject('movie_lister')
async def get_names2(movie_lister):
    return movie_lister.list_real_names()


@ctx.async_service('foo')
async def _get_foo():
    return 'foo'


@ctx.inject('foo')
async def get_foo(foo):
    return foo


@ws.async_service('bar')
async def _get_bar():
    return 'bar'


@ws2.inject('bar')
async def get_bar(bar):
    return bar


ctx.workspace(ws)
ctx.workspace(ws2)


@pytest.mark.asyncio
async def test_async_inject():
    actual = await get_names()
    expect = ['Peter', 'Tony']
    assert actual == expect


@pytest.mark.asyncio
async def test_async_inject_cache():
    instance1 = await get_names()
    instance2 = await get_names2()
    assert instance1 == instance2


@pytest.mark.asyncio
async def test_async_factory():
    assert await get_foo() == 'foo'


@pytest.mark.asyncio
async def test_async_inject_from_the_third_workspace():
    actual = await get_bar()
    assert actual == 'bar'
