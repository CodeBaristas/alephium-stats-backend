# NOTE:actual no db necessary
# import asyncio as aio
import uvicorn

# NOTE:actual no db necessary
# from sqlmodel import SQLModel
# from .deps import DDB, inject
# from .common import db_engine
from .config import config
from .utils.utils import init_logger

# NOTE:actual no db necessary
# @inject
# async def init_db(db=DDB):
#     # DATABASE
#     if config.APP_CONFIG == "dev":
#         async with db_engine.begin() as c:
#             await c.run_sync(SQLModel.metadata.create_all)


def main():
    init_logger(config.APP_LOG_LEVEL, config.APP_LOGGING_IGNORE)
    # NOTE:actual no db necessary
    # aio.run(init_db())

    uvicorn.run(
        "alephium_stats.app:app",
        host="0.0.0.0",
        port=8000,
        workers=1 if config.APP_DEBUG else config.APP_WORKER,
        log_level=config.APP_LOG_LEVEL.lower(),
        reload=config.APP_DEBUG,
    )


if __name__ == "__main__":
    main()
