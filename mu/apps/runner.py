# -*- coding: utf-8 -*-
from functools import partial
from asyncio import get_event_loop

from autobahn.wamp.types import ComponentConfig
from autobahn.websocket.protocol import parseWsUrl
from autobahn.asyncio.websocket import WampWebSocketClientFactory

import txaio
txaio.use_asyncio()


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

    def run(self, sessions=[]):

        # 1) factory for use ApplicationSession
        def create(callable):
            cfg = ComponentConfig(self.realm, self.extra)
            try:
                session = callable(cfg)
            except Exception as e:
                # the app component could not be created .. fatal
                print(e)
                get_event_loop().stop()
            else:
                session.debug_app = self.debug_app
                return session

        isSecure, host, port, resource, path, params = parseWsUrl(self.url)

        # 2) create a WAMP-over-WebSocket transport client factories
        factories = []
        for session in sessions:
            factory = partial(create, callable=session)
            factories.append(
                WampWebSocketClientFactory(
                    factory,
                    url=self.url,
                    serializers=self.serializers,
                    debug=self.debug,
                    debug_wamp=self.debug_wamp
                )
            )

        # 3) start the service clients
        loop = get_event_loop()
        txaio.use_asyncio()
        txaio.config.loop = loop
        for transport_factory in factories:
            coro = loop.create_connection(
                transport_factory,
                host,
                port,
                ssl=isSecure
            )
            loop.run_until_complete(coro)

        # 4) now enter the asyncio event loop
        loop.run_forever()
        loop.close()
