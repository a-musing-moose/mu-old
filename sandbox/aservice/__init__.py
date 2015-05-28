# -*- coding: utf-8 -*-
from mu.apps import AppConfig
from .components import TestComponent
from .commands import Moo


class AServiceConfig(AppConfig):
    name = "A Test Service"
    label = "aservice"
    session_class = TestComponent

    def get_commands(self):
        return [Moo()]


config = AServiceConfig()
