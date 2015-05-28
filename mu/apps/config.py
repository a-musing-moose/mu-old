# -*- coding: utf-8 -*-
from ..loading import load_from_path


class AppConfig(object):
    session_class = None
    name = None
    label = None

    def get_session_class(self):
        return self.session_class

    def get_label(self):
        return self.label

    def get_name(self):
        return self.name

    def get_commands(self):
        return []
