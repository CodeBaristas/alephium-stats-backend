# NOTE:actual no db necessary
# from sqlalchemy.ext.asyncio import create_async_engine
from redis import asyncio as aioredis
from slowapi import Limiter
from slowapi.util import get_remote_address

from .config import config
from .utils.alephium.explorer import AlephiumExplorer
from .utils.alephium.node import AlephiumNode

# ################################################################################
# # DB
# db_engine = create_async_engine(config.DB_URL, **config.DB_ENGINE_CONFIG)

################################################################################
# REDIS
redis = aioredis.from_url(config.REDIS_URL, encoding="utf8", decode_responses=True)

##############################################################################
# RATE LIMITER
limiter = Limiter(key_func=get_remote_address)

##############################################################################
# ALEPHIUM
alph_node = AlephiumNode(config.ALEPHIUM_NODE_URL, config.ALEPHIUM_NODE_API_KEY)
alph_explorer = AlephiumExplorer(config.ALEPHIUM_EXPLORER_URL)
