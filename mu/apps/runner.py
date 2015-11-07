# -*- coding: utf-8 -*-
import signal

from functools import partial
from asyncio import get_event_loop

from autobahn.wamp.types import ComponentConfig
from autobahn.websocket.protocol import parseWsUrl
from autobahn.asyncio.websocket import WampWebSocketClientFactory

import txaio
txaio.use_asyncio()


def _factory_builder(callable, config, debug_app=False):
    try:
        session = callable(config)
    except Exception as e:
        print(e)
        get_event_loop().stop()
    else:
        session.debug_app = debug_app
        return session


class SessionsRunner(object):

    def __init__(self, url, realm, extra=None, serializers=None, debug=False,
                 debug_wamp=False, debug_app=False):
        """
        :param url: The WebSocket URL of the WAMP router to connect to
        :type url: unicode
        :param realm: The WAMP realm to join the application session to.
        :type realm: unicode
        :param extra: Optional extra configuration to forward to services
        :type extra: dict
        :param serializers: A list of WAMP serializers to use
        :type serializers: list
        :param debug: Turn on low-level debugging.
        :type debug: bool
        :param debug_wamp: Turn on WAMP-level debugging.
        :type debug_wamp: bool
        :param debug_app: Turn on app-level debugging.
        :type debug_app: bool
        """
        self.url = url
        self.realm = realm
        self.extra = extra or dict()
        self.debug = debug
        self.debug_wamp = debug_wamp
        self.debug_app = debug_app
        self.make = None
        self.serializers = serializers

    def run(self, app_sessions=[]):

        isSecure, host, port, resource, path, params = parseWsUrl(self.url)

        cfg = ComponentConfig(self.realm, self.extra)
        factories = []
        for app_session in app_sessions:
            factory = partial(
                _factory_builder,
                callable=app_session,
                config=cfg,
                debug_app=self.debug_app
            )
            factories.append(
                WampWebSocketClientFactory(
                    factory,
                    url=self.url,
                    serializers=self.serializers,
                    debug=self.debug,
                    debug_wamp=self.debug_wamp
                )
            )

        loop = get_event_loop()
        txaio.use_asyncio()
        txaio.config.loop = loop

        protocols = []
        for transport_factory in factories:
            coro = loop.create_connection(
                transport_factory,
                host,
                port,
                ssl=isSecure
            )
            (_, protocol) = loop.run_until_complete(coro)
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

        # give Goodbye message a chance to go through, if we still
        # have an active session
        for protocol in protocols:
            if protocol._session:
                loop.run_until_complete(protocol._session.leave())

        loop.close()
