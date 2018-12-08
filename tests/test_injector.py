# -*- coding: utf-8 -*-

import conveyor

ctx = conveyor.Context('testing')


@ctx.service('movie_finder')
class MovieFinder:
    @ctx.inject('dummy_list')
    def __init__(self, dummy_list):
        self._l = dummy_list

    def find_all(self):
        return self._l.show()


@ctx.service('dummy_list')
class DummyList:
    @staticmethod
    def show():
        return ['Inception', 'The Dark Knight']


@ctx.service(key='movie_lister')
class MovieLister:

    @ctx.inject('movie_finder')
    def __init__(self, movie_finder: MovieFinder):
        self._movie_finder = movie_finder

    def find_all(self):
        return self._movie_finder.find_all()


@ctx.inject('movie_lister')
def get_movies(movie_lister: MovieLister):
    return movie_lister.find_all()


def test_injector():
    actual = get_movies()
    expect = ['Inception', 'The Dark Knight']
    assert actual == expect
