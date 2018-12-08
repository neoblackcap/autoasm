# -*- coding: utf-8 -*-


class ConveyorError(Exception):
    pass


class ServiceNotFound(ConveyorError):
    pass


class ServiceDuplicated(ConveyorError):
    pass


class NoConfig(ConveyorError):
    pass
