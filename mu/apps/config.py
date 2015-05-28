# -*- coding: utf-8 -*-


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
