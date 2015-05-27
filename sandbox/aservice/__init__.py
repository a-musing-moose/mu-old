# -*- coding: utf-8 -*-
from mu.services import ServiceConfig


class AServiceConfig(ServiceConfig):
    name = "A Test Service"
    label = "aservice"
    component_path = 'aservice.components.TestComponent'


config = AServiceConfig
