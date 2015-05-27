import os
import yaml
from collections import OrderedDict

from .loading import load_from_path


class Settings(object):

    def __init__(self):
        self._data = None
        self._services = OrderedDict()

    @property
    def _loaded(self):
        if self._data is None:
            return False
        return True

    def _setup(self):
        source = os.environ.get("MU_SETTINGS", None)
        if source is None:
            raise Exception("MU_SETTINGS has not been defined")
        with open(source, "r") as f:
            self._data = yaml.safe_load(f)
        self._load_services()

    def _load_services(self):
        for path in self.services:
            path += ".config"
            config = load_from_path(path)(self)
            label = config.get_label()
            if label in self._services.keys():
                raise Exception(
                    "you have more than one service with the label {}".format(
                        label
                    )
                )
            self._services[config.get_label()] = config

    def get_services(self):
        if self._loaded is False:
            self._setup()
        return self._services

    def get_service(self, name):
        return self._services[name]

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
