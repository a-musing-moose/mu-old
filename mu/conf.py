import os
import json


class Settings(object):

    name = None
    realm = 'default'
    router_dsn = 'ws://localhost:8080/ws'

    def __init__(self):
        source = os.environ.get("MU_SETTINGS", None)
        if source is None:
            raise Exception("MU_SETTINGS has not been defined")
        try:
            self.json = json.loads(source)
        except ValueError:
            with open(source, 'r') as f:
                self.json = json.load(f)

    def __getattr__(self, key):
        try:
            setattr(self, key, self.json[key])
        except:
            raise AttributeError()
        if isinstance(self.key, dict) and 'env' in self.key:
            default = self.key.get('default', None)
            setattr(self, key, self._from_environment(
                self.key['env'],
                default
            ))
        return getattr(self, key)

    def _from_environment(self, key, default=None):
        try:
            return os.environ[key]
        except KeyError:
            return default


settings = Settings()
