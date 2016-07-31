# -*- coding: utf-8 -*-
from asyncio import get_event_loop, sleep
from random import randint

from autobahn.asyncio.wamp import ApplicationSession


class TestComponent(ApplicationSession):

    async def onJoin(self, details):
        self.running = True
        print("[A] Service Joined realm: {0}, session id: {1}".format(
            details.realm,
            details.session
        ))
        self.loop = get_event_loop()
        await self.send_ping()

    async def send_ping(self):
        delay = randint(1, 5)
        print("<--- [A] sleeping for {} seconds".format(delay))
        await sleep(delay)
        if self.is_attached():
            await self.call("b.ping", "A")
            self.loop.create_task(self.send_ping())
