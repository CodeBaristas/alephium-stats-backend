import asyncio

from fastapi_websocket_pubsub import PubSubClient


async def on_trigger(**kwargs):
    print(kwargs)
    print("Trigger URL was accessed with data")


async def subscribe_to_trigger():
    async with PubSubClient(server_uri="ws://localhost:8000/streams/blocks") as client:
        client.subscribe("block_data", on_trigger)
        await asyncio.Event().wait()


asyncio.run(subscribe_to_trigger())
