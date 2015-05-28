# -*- coding: utf-8 -*-
from mu.apps import AppConfig
from .components import TestComponent


class BServiceConfig(AppConfig):
    name = "B Test Service"
    label = "bservice"
    session_class = TestComponent


config = BServiceConfig()
