import asyncio as aio
import json

from httpx import AsyncClient

from ..common import redis
from ..config import config
from ..run_worker import celery

# from ..utils.utils import logger

loop = aio.get_event_loop()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **_):  # pragma: no cover
    # execute each seconds
    sender.add_periodic_task(
        config.ALEPHIUM_EXPLORER_REFRESH_SECONDS,
        check_new_node_data.s(),
    )


@celery.task
def check_new_node_data():  # pragma: no cover
    loop.run_until_complete(_check_new_node_data())


async def _check_new_node_data():
    async with AsyncClient() as requests:
        response = await requests.get(
            str(config.ALEPHIUM_EXPLORER_URL + "/blocks"),
            params={"limit": config.ALEPHIUM_EXPLORER_MAX_REQUEST_BLOCKS},
        )
        data = response.json()
        response_blocks = data.get("blocks")
        response_hashes = [block["hash"] for block in data.get("blocks")]

        stored_hashes = await redis.get("hash")

        new_hashes = response_hashes
        if stored_hashes is not None:
            new_hashes = [
                hash_value
                for hash_value in response_hashes
                if hash_value not in stored_hashes
            ]
        old_hashes = [
            hash_value for hash_value in response_hashes if hash_value not in new_hashes
        ]

        if new_hashes:
            old_hashes.extend(new_hashes)
            await redis.set("hash", json.dumps(old_hashes))

            new_blocks = [
                block for block in response_blocks if block["hash"] in new_hashes
            ]
            [
                await requests.post(config.ALEPHIUM_EXPLORER_TRIGGER_ROUTE, json=block)
                for block in new_blocks
            ]
