# -*- coding: utf-8 -*-
import functools
import threading

from . import execptions


class Context:

    def __init__(self, name):
        self._name = name
        self._config = None
        self._lock = threading.RLock()
        self._dependencies = {}
        self._entities = {}

    def __str__(self):
        return self._name

    def service(self, key):

        def wrap(klass):
            self._register(klass, key)
            return klass

        return wrap

    def inject(self, *keys):

        def wrapper(func):
            @functools.wraps(func)
            def wrap(*args, **kwargs):
                instances = {key: self._resolve(key) for key in keys}
                injection = set(keys) - set(kwargs.keys())
                kwargs.update({key: instances[key] for key in injection})
                return func(*args, **kwargs)

            return wrap

        return wrapper

    def _resolve(self, key):
        if not self._entities.get(key):
            with self._lock:
                return self._resolve_unsafe(key)
        return self._entities.get(key)

    def _resolve_unsafe(self, key):
        try:
            return self._entities[key]
        except KeyError:
            # no initialized instance
            pass

        dependency = self._dependencies.get(key)
        if not dependency:
            msg = f"can't find dependency with key {key}"
            raise execptions.ServiceNotFound(msg)

        entity = dependency()
        self._entities[key] = entity
        return self._entities[key]

    def _register(self, cls, key):
        if not self._dependencies.get(key):
            with self._lock:
                if not self._dependencies.get(key):
                    self._dependencies[key] = cls
                    return

        entity_type = type(self._dependencies.get('key'))
        msg = f'{key} is registered and type is {entity_type}, ' \
            f'but get new registration with {type(cls)}'
        raise execptions.ServiceNotFound(msg)

    def workspace(self, ws: 'Workspace'):
        self._dependencies.update(ws._dependencies)
        ws.bind(self)


class Workspace(Context):

    def __init__(self, name):
        super().__init__(name)
        self._context: Context = None

    def bind(self, ctx: Context):
        self._context = ctx

    def inject(self, *keys):
        def _inject(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if self._context:
                    return self._context.inject(*keys)(func)(*args, **kwargs)
                raise execptions.WorkspaceNotBinding()

            return wrapper

        return _inject
