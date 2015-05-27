# -*- coding: utf-8 -*-
from ..loading import load_from_path


class ServiceConfig(object):
    component_path = None
    name = None
    label = None

    def __init__(self, settings):
        self._component = None
        self.settings = settings

    def get_component(self):
        if self.loaded is False:
            self._component = load_from_path(self.component_path)
        return self._component

    def get_label(self):
        return self.label

    def get_name(self):
        return self.name

    @property
    def loaded(self):
        if self._component is None:
            return False
        return True
