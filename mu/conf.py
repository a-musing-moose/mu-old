import os
import re
from collections import OrderedDict

import yaml

from mu.utils.loading import load_from_path


class Settings(object):

    env_pattern = re.compile(
        r'\$\{(?P<env_var>\w*)(?::(?P<default>[^}]*))?\}$'
    )

    def __init__(self):
        self._data = None
        self._apps = OrderedDict()
        yaml.SafeLoader.add_constructor('!envex', self._envex_constructor)
        yaml.SafeLoader.add_implicit_resolver(
            "!envex",
            self.env_pattern,
            first=['$']
        )

    def _envex_constructor(self, loader, node):
        value = loader.construct_scalar(node)
        result = self.env_pattern.match(value)

        env_var = result.group('env_var')
        default = result.group('default') or ""
        try:
            value = os.environ[env_var]
        except KeyError:
            value = default
        return value

    @property
    def _loaded(self):
        return self._data is not None

    def _setup(self):
        source = os.environ.get("MU_SETTINGS", None)
        if source is None:
            raise Exception("MU_SETTINGS has not been defined")
        with open(source, "r") as f:
            self._data = yaml.safe_load(f)
        self._load_apps()

    def _load_apps(self):
        for path in self.apps:
            path += ".config"
            config = load_from_path(path)
            label = config.get_label()
            if label in self._apps.keys():
                raise Exception(
                    "you have more than one app with the label {}".format(
                        label
                    )
                )
            self._apps[config.get_label()] = config

    def get_apps(self):
        if self._loaded is False:
            self._setup()
        return self._apps

    def get_app(self, name):
        if self._loaded is False:
            self._setup()
        return self._apps[name]

    def get_session_classes(self):
        sessions = []
        for service in self.get_apps().values():
            session = service.get_session_class()
            if session is not None:
                sessions.append(session)
        return sessions

    def get_commands(self):
        commands = []
        for service in self.get_apps().values():
            commands += service.get_commands()
        return commands

    def __getattr__(self, key):
        if self._loaded is False:
            self._setup()
        try:
            value = self._data[key]
        except KeyError:
            raise AttributeError(key)
        if isinstance(value, dict) and 'env' in value:
            default = value.get('default', None)
            value = self._from_environment(
                value['env'],
                default
            )
        setattr(self, key, value)
        return value

    def _from_environment(self, key, default=None):
        """
        Attempts to get the value from an environmental variable
        """
        try:
            return os.environ[key]
        except KeyError:
            return default


settings = Settings()
