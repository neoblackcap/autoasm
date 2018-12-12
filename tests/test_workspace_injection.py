# -*- coding: utf-8 -*-
import autoasm

ctx = autoasm.Context('testing')
ws = autoasm.Workspace('testing')


@ws.service('movie_finder')
class MovieFinder:
    def __init__(self):
        self._names = ['Peter', 'Tony']

    def list_real_names(self):
        return self._names


@ws.service('movie_lister')
class MovieLister:

    @ws.inject('movie_finder')
    def __init__(self, movie_finder: MovieFinder):
        self._movie_finder = movie_finder

    def list_real_names(self):
        return self._movie_finder.list_real_names()


@ctx.service('movie_lister2')
class MovieLister2:
    @ctx.inject('movie_finder')
    def __init__(self, movie_finder: MovieFinder):
        self._movie_finder = movie_finder

    def list_real_names(self):
        return self._movie_finder.list_real_names()


ctx.workspace(ws)


@ctx.inject('movie_lister2')
def get_names(movie_lister2):
    return movie_lister2.list_real_names()


@ws.inject('movie_lister2')
def get_names2(movie_lister2):
    return movie_lister2.list_real_names()


def test_from_main_context_inject_workspace_service():
    assert get_names() == ['Peter', 'Tony']


def test_from_workspace_inject_main_context_service():
    assert get_names2() == ['Peter', 'Tony']
