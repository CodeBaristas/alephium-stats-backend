from celery import Celery

from .config import APP_NAME, config

celery = Celery(
    APP_NAME,
    broker=config.REDIS_URL,
)


from alephium_stats.websocket.tasks import *  # noqa: F401,E402
