# -*- coding: utf-8 -*-


class AutoasmError(Exception):
    pass


class ServiceNotFound(AutoasmError):
    pass


class ServiceDuplicated(AutoasmError):
    pass


class NoConfig(AutoasmError):
    pass


class WorkspaceNotBinding(AutoasmError):
    pass
