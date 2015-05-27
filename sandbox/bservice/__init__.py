# -*- coding: utf-8 -*-
from mu.services import ServiceConfig


class BServiceConfig(ServiceConfig):
    name = "B Test Service"
    label = "bservice"
    component_path = 'bservice.components.TestComponent'


config = BServiceConfig
