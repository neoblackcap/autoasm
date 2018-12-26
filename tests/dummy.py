# -*- coding: utf-8 -*-
from .base import ws


@ws.service('foo')
def get_name():
    return 'bar'
