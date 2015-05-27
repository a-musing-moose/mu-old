# -*- coding: utf-8 -*-
from asyncio import sleep, get_event_loop, async, coroutine
from random import randint
from autobahn.asyncio.wamp import ApplicationSession


class TestComponent(ApplicationSession):

    @coroutine
    def onJoin(self, details):
        print("A Service Joined realm: {0}, session id: {1}".format(
            details.realm,
            details.session
        ))
        self.loop = get_event_loop()
        yield from self.register(self.on_ping, "a.ping")
        yield from self.send_ping()

    def on_ping(self, name):
        print("---> A got ping from {}".format(name))

    @coroutine
    def send_ping(self):
        delay = randint(1, 5)
        print("<--- A sleeping for {} seconds".format(delay))
        yield from sleep(delay)
        yield from self.call("b.ping", "A")
        self.loop.call_soon_threadsafe(async, self.send_ping())
