import logging
import signal
from asyncio import Task, get_event_loop
from functools import partial

import txaio
from autobahn.asyncio.websocket import WampWebSocketClientFactory
from autobahn.wamp.types import ComponentConfig
from autobahn.websocket.util import parse_url

log = logging.getLogger(__name__)


def _factory_builder(callable, config, debug_app=False):
    try:
        session = callable(config)
    except Exception as e:
        log.exception(e)
        get_event_loop().stop()
    else:
        session.debug_app = debug_app
        return session

protocols = []


class SessionsRunner(object):

    def __init__(self, url, realm, extra=None, serializers=None, ssl=None):
        """
        :param url: The WebSocket URL of the WAMP router to connect to
        :type url: unicode
        :param realm: The WAMP realm to join the application session to.
        :type realm: unicode
        :param extra: Optional extra configuration to forward to services
        :type extra: dict
        :param serializers: A list of WAMP serializers to use
        :type serializers: list
        :param ssl: An (optional) SSL context instance or a bool
        :type ssl: :class:`ssl.SSLContext` or bool
        """
        self.url = url
        self.realm = realm
        self.extra = extra or dict()
        self.make = None
        self.serializers = serializers
        self.ssl = ssl

    def run(self, app_sessions=[]):

        isSecure, host, port, resource, path, params = parse_url(self.url)

        if self.ssl is None:
            ssl = isSecure
        else:
            if self.ssl and not isSecure:
                raise RuntimeError(
                    "ssl argument is True but using ws: protocol"
                )
            ssl = self.ssl

        cfg = ComponentConfig(self.realm, self.extra)
        factories = []
        for app_session in app_sessions:
            factory = partial(
                _factory_builder,
                callable=app_session,
                config=cfg
            )
            factories.append(
                WampWebSocketClientFactory(
                    factory,
                    url=self.url,
                    serializers=self.serializers
                )
            )

        loop = get_event_loop()
        txaio.use_asyncio()
        txaio.config.loop = loop

        for transport_factory in factories:
            coro = loop.create_connection(
                transport_factory,
                host,
                port,
                ssl=ssl
            )
            _, protocol = loop.run_until_complete(coro)
            protocols.append(protocol)

        try:
            loop.add_signal_handler(signal.SIGTERM, loop.stop)
        except NotImplementedError:
            # signals are not available on Windows
            pass

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            # wait until we send Goodbye if user hit ctrl-c
            # (done outside this except so SIGTERM gets the same handling)
            pass

        close_loop_cleanly()


def close_loop_cleanly():
    log.debug("closing event loop")
    loop = get_event_loop()
    for protocol in protocols:
        if protocol._session:
            loop.run_until_complete(protocol._session.leave())

    for task in Task.all_tasks():
        loop.run_until_complete(task)
    loop.close()
    log.debug("event loop closed")
