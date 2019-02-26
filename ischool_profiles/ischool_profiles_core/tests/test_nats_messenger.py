from django.test import TestCase
from ..utils import publish_message_async
from nats.aio.client import Client as NATS
import asyncio
import json
from django.conf import settings


async def subscriber(loop, subscribe_handler):
    options = {
        "servers": settings.NATS_SERVERS,
        "loop": loop,
        "dont_randomize": True,
        "reconnect_time_wait": 2,
        "max_reconnect_attempts": 5,
    }

    nc = NATS()
    try:
        await nc.connect(**options)
    except ErrNoServers as e:
        # Could not connect to any server in the cluster.
        print(e)
        return

    if nc.is_connected:
        await nc.subscribe(settings.NATS_BASE_SERVICE_SUBJECT + ".test", cb=subscribe_handler) 


class NatsMessengerTestCase(TestCase):

    def subscribe_handler(self, fut):
        def callback(msg):
            fut.set_result(json.loads(msg.data))
        return callback

    def test_send(self):
        async def run(loop):
            fut = loop.create_future()
            res = await subscriber(loop, self.subscribe_handler(fut))
            #res2 = await self.nats.send({"message": "Does this work?"})
            res2 = await publish_message_async(loop, "test", {"message": "Does this work?"})
            result = await fut
            return result
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(run(loop))
        self.assertEqual(res["message"], "Does this work?")