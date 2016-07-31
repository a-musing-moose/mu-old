from asyncio import get_event_loop

from autobahn.asyncio.wamp import ApplicationSession


class TestComponent(ApplicationSession):

    async def onJoin(self, details):
        print("B Service Joined realm: {0}, session id: {1}".format(
            details.realm,
            details.session
        ))
        self.loop = get_event_loop()
        await self.register(self.on_ping, "b.ping")

    async def on_ping(self, name):
        print("---> B got ping from {}".format(name))
