# -*- coding: utf-8 -*-
"""
    autoasm
    ~~~~~~~
    A simple dependency injection framework

    :copyright: © 2018 by Neo Ko
    :license: Apache 2.0, see LICENSE for more details.
"""

import asyncio
import enum
import functools
import threading

from . import config
from . import execptions


class ContextType(enum.Enum):
    ASYNC = 1
    SYNC = 2


class ServiceType(enum.Enum):
    ASYNC = 1
    SYNC = 2


CoerceType = config.CoerceType


class Empty:
    pass


_EMPTY = Empty()


class Context:
    """
    autoasm core class, create a context to get dependency
    """

    def __init__(self, name, ctx_type=ContextType.SYNC, loop=None):
        """

        :param str name:
        :param ContextType ctx_type:
        :param loop:
        """
        self._name = name
        self._config = {}
        self._lock = threading.RLock()
        self._alock = asyncio.Lock()
        self._dependencies = {}
        self._async_dependencies = {}
        self._entities = {}
        self._type = ctx_type
        if self._type == ContextType.ASYNC:
            if isinstance(loop, asyncio.AbstractEventLoop):
                self._loop = loop
            else:
                self._loop = asyncio.get_event_loop()

    def __str__(self):
        return self._name

    @property
    def config(self):
        return self._config

    def configure_from_module(self, name, coerce_type=CoerceType.SAME):
        cfg = config.ModuleConfig(name, coerce_type)
        self.configure(cfg)

    def configure_from_json(self, path):
        cfg = config.JsonConfig(path)
        self.configure(cfg)

    def configure(self, cfg):
        """

        :param config.Config cfg:
        :return:
        """

        self._config.update(cfg.to_dict())

    def service(self, key):

        def wrap(runnable):
            self._register(runnable, key, service_type=ServiceType.SYNC)
            return runnable

        return wrap

    def async_service(self, key):
        def wrap(runnable):
            self._register(runnable, key, service_type=ServiceType.ASYNC)
            return runnable

        return wrap

    def inject(self, *keys):

        def wrapper(func):

            @functools.wraps(func)
            def wrap(*args, **kwargs):
                instances = {key: self._resolve(key) for key in keys}
                injection = set(keys) - set(kwargs.keys())
                kwargs.update({key: instances[key] for key in injection})
                return func(*args, **kwargs)

            @functools.wraps(func)
            async def async_wrap(*args, **kwargs):
                instances = {key: await self._async_resolve(key) for key in
                             keys}
                injection = set(keys) - set(kwargs.keys())
                kwargs.update({key: instances[key] for key in injection})
                return await func(*args, **kwargs)

            if asyncio.iscoroutinefunction(func):
                return async_wrap
            else:
                return wrap

        return wrapper

    def _resolve(self, key):
        with self._lock:
            if not _is_empty(self._config, key):
                return self._config.get(key)
            elif _is_empty(self._entities, key):
                return self._resolve_unsafe(key)
            return self._entities.get(key)

    def _resolve_unsafe(self, key):
        dependency = self._dependencies.get(key)
        if not dependency:
            _msg = "can't find dependency with key {key}"
            msg = _msg.format(key=key)
            raise execptions.ServiceNotFound(msg)

        entity = dependency()
        self._entities[key] = entity
        return self._entities[key]

    async def _async_resolve(self, key):
        async with self._alock:
            if not _is_empty(self._config, key):
                return self._config.get(key)
            elif _is_empty(self._entities, key):
                return await self._async_resolve_unsafe(key)
            return self._entities.get(key)

    async def _async_resolve_unsafe(self, key):
        async_dep = self._async_dependencies.get(key)

        if async_dep:
            entity = await async_dep()
            self._entities[key] = entity
            return self._entities[key]
        elif self._dependencies.get(key):
            dep = self._dependencies.get(key)
            entity = dep()
            self._entities[key] = entity
            return self._entities[key]

        _msg = "can't find dependency with key {key}"
        msg = _msg.format(key=key)
        raise execptions.ServiceNotFound(msg)

    def _register(self, runnable, key, service_type=ServiceType.SYNC):
        """

        :param typing. runnable:
        :param key:
        :param ServiceType service_type:
        :return:
        """
        with self._lock:
            if service_type == ServiceType.SYNC:
                if _is_empty(self._dependencies, key):
                    self._dependencies[key] = runnable
                    return
            elif service_type == ServiceType.ASYNC:
                if _is_empty(self._async_dependencies, key):
                    self._async_dependencies[key] = runnable
                    return
            else:
                raise TypeError('unknown service_type')

            entity_type = type(self._dependencies.get('key'))
            _msg = '{key} is registered and type is {entity_type}, ' \
                   'but get new registration with {t}'
            msg = _msg.format(key=key,
                              entity_type=entity_type,
                              t=type(runnable))

            raise execptions.ServiceDuplicated(msg)

    def workspace(self, ws):
        """

        :param Workspace ws:
        :return:
        """
        self._dependencies.update(ws._dependencies)
        self._async_dependencies.update(ws._async_dependencies)
        ws.bind(self)


class Workspace(Context):

    def __init__(self, name):
        super().__init__(name)
        # type: Context
        self._context = None

    def bind(self, ctx):
        """

        :param Context ctx:
        :return:
        """
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


def _is_empty(container, key):
    """

    :param typing.Mapping container:
    :param str key:
    :return:
    """
    return isinstance(container.get(key, _EMPTY), Empty)
