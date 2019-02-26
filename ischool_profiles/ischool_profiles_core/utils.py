import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import logging
import json
from django.conf import settings

logger = logging.getLogger(__name__)



async def publish_message_async(loop, subject, json_data):
    """ Helper Class for sending messages to our nats setup
    """
    nc = NATS()


    options = {
        "servers": settings.NATS_SERVERS,
        "loop": loop,
        "dont_randomize": True,
        "reconnect_time_wait": 2,
        "max_reconnect_attempts": 5,
    }
    try:
        await nc.connect(**options)
        logger.info("Connected to NATS")
    except ErrNoServers as e:
        # Could not connect to any server in the cluster.
        logger.error(e)
        return

    if nc.is_connected:
        logger.info("Sending message to NATS")
        try:
            await nc.publish(settings.NATS_BASE_SERVICE_SUBJECT + "." + subject, json.dumps(json_data).encode())
            logger.info("Message Successfully Sent")
        except ErrConnectionClosed:
            print("Can't publish since no longer connected.")

def publish_message(subject, json_data):
    loop = asyncio.new_event_loop()
    loop.run_in_executor(publish_message_async(loop, subject, json_data))
    return