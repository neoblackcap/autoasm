# -*- coding: utf-8 -*-
import asyncio

import pytest

import autoasm

ctx = autoasm.Context('testing')


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
