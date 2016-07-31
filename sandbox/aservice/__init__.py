# -*- coding: utf-8 -*-
from mu.apps import AppConfig

from .commands import Moo
from .components import TestComponent


class AServiceConfig(AppConfig):
    name = "A Test Service"
    label = "aservice"
    session_class = TestComponent

    def get_commands(self):
        return [Moo()]


config = AServiceConfig()
