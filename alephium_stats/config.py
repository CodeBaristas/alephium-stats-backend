import os
from typing import ClassVar, List

from dimfred.config import BaseConfig

APP_CONFIG = os.environ["APP_CONFIG"]
APP_NAME = os.environ["APP_NAME"]


class Config(BaseConfig):
    ############################################################################
    # ALEPHIUMNODE
    ALEPHIUM_NODE_API_KEY: str
    ALEPHIUM_NODE_URL: str = "https://alephiumfullnode.fresenius.ai"
    ALEPHIUM_HEADER: ClassVar[dict] = {
        "accept": "application/json",
        "X-API-KEY": "",
    }

    ############################################################################
    # ALEPHIUMEXPLORER
    ALEPHIUM_EXPLORER_URL: str = "https://explorer.fresenius.ai"
    ALEPHIUM_EXPLORER_TRIGGER_ROUTE: str
    ALEPHIUM_EXPLORER_REFRESH_SECONDS: int = 1
    ALEPHIUM_EXPLORER_BLOCK_SEND_RATE_SECONDS: float = 0.5
    ALEPHIUM_EXPLORER_MAX_REQUEST_BLOCKS: int = 10

    ############################################################################
    # FRONTEND
    FRONTEND_API_KEY: str

    ############################################################################
    # APP
    APP_DEBUG: bool = False
    APP_WORKER: int = 1
    APP_LOG_LEVEL: str = "INFO"
    APP_LOGGING_IGNORE: List[str] = [
        "aiosqlite",
        "asyncio",
        "filelock",
        "httpx",
        "urllib3",
        "uvicorn.protocols.http",
        "websockets",
    ]
    APP_CONFIG: str

    ############################################################################
    # SERVICES
    # NOTE:actual no db necessary
    # DB_URL: str = f"sqlite+aiosqlite:///data/{APP_NAME}.db"
    # DB_ENGINE_CONFIG: dict = {
    #     "echo": False,
    #     "future": True,
    #     "pool_recycle": 7200,
    #     "pool_reset_on_return": None,
    # }
    # DB_SESSION_CONFIG: dict = {
    #     "expire_on_commit": False,
    # }
    REDIS_URL: str

    FAPI_DOCS_ENABLE: bool = True
    FAPI_CORS_ENABLE: bool = True
    FAPI_CORS_ALLOW_CREDENTIALS: bool = True
    FAPI_CORS_ALLOW_ORIGINS: List[str] = ["*"]
    FAPI_CORS_ALLOW_METHODS: List[str] = ["*"]
    FAPI_CORS_ALLOW_HEADERS: List[str] = ["*"]

    def init(self):
        self.ALEPHIUM_HEADER["X-API-KEY"] = self.ALEPHIUM_NODE_API_KEY


config = Config()
config.init()
