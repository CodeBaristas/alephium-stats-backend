import asyncio as aio
import os

# NOTE:actual no db necessary
# import random
from pathlib import Path

import pytest as pt
from httpx import AsyncClient

# NOTE:actual no db necessary
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlmodel import SQLModel

os.environ["APP_CONFIG"] = "tests"
os.environ["APP_NAME"] = "alephium_stats"


from alephium_stats.config import config

# NOTE:actual no db necessary
# from alephium_stats.crud import CRUD
from alephium_stats.utils.utils import init_logger

# include all fixtures from the fixtures dir
for file_path in Path("tests/fixtures").glob("*"):
    module_name = file_path.stem
    try:
        exec(f"from tests.fixtures.{module_name} import *")
    # can happen for non .py fixtures
    except ModuleNotFoundError:
        pass


################################################################################
# ASYNCIO
@pt.fixture
def anyio_backend():
    return "asyncio"


@pt.fixture(scope="session")
def event_loop():
    loop = aio.get_event_loop()
    yield loop
    loop.close()


################################################################################
# FASTAPI
@pt.fixture
def patch_client():
    async def patched_delete(self, *args, **kwargs):
        return await self.request("DELETE", *args, **kwargs)

    AsyncClient.delete = patched_delete


@pt.fixture
# NOTE:actual no db necessary
# async def client(event_loop, db, fastapi_dep, patch_client):
async def client(event_loop, fastapi_dep, patch_client):
    from alephium_stats.app import app

    # NOTE:actual no db necessary
    # from alephium_stats.deps import aget_db
    # async def patch_aget_db():
    #     return db
    # with fastapi_dep(app).override({aget_db: patch_aget_db}):
    # with fastapi_dep(app):
    async with AsyncClient(app=app, base_url="http://test") as client_:
        yield client_


################################################################################
# DB
# NOTE:actual no db necessary
# async def create_db(engine, db_name):
#     from sqlmodel import text
#
#     async with engine.connect() as c:
#         try:
#             await c.execute(text(f"create database {db_name};"))
#             await c.execute(text("SET GLOBAL max_connections=2000;"))
#         except Exception:
#             pass
#
#
# async def drop_db(engine, db_name):
#     from sqlmodel import text
#
#     async with engine.connect() as c:
#         try:
#             await c.execute(text(f"drop database {db_name};"))
#         except Exception:
#             pass


# NOTE:actual no db necessary
# @pt.fixture(scope="function")
# async def db_engine(mocker):
#     # LOGGING
#     init_logger(config.APP_LOG_LEVEL, config.APP_LOGGING_IGNORE)
#
#     if "sqlite" in config.DB_URL:
#         engine = create_async_engine(config.DB_URL)
#         async with engine.begin() as c:
#             await c.run_sync(SQLModel.metadata.create_all)
#             yield engine
#             await c.run_sync(SQLModel.metadata.drop_all)
#
#     else:
#         db_url, db_name = config.DB_URL.rsplit("/", 1)
#         db_name = f"{db_name}_{random.randint(0, 1000000000000000000000)}"
#         new_url = f"{db_url}/{db_name}"
#         mocker.patch("alephium_stats.config.DB_URL", new_url)
#
#         base_engine = create_async_engine(db_url, **config.DB_ENGINE_CONFIG)
#         engine = create_async_engine(new_url, **config.DB_ENGINE_CONFIG)
#         mocker.patch("alephium_stats.common.db_engine", engine)
#
#         await create_db(base_engine, db_name)
#         async with engine.begin() as c:
#             await c.run_sync(SQLModel.metadata.create_all)
#             # WITH ALEMBIC
#             # alembic_cfg = alembic.config.Config("alembic_tests.ini")
#             # alembic.command.upgrade(alembic_cfg, "head")
#
#         yield engine
#
#         async with engine.begin() as c:
#             await c.run_sync(SQLModel.metadata.drop_all)
#         await drop_db(base_engine, db_name)


# NOTE:actual no db necessary
# @pt.fixture(scope="function")
# async def db(db_engine):
#     make_session = sessionmaker(db_engine, class_=CRUD, **config.DB_SESSION_CONFIG)
#     async with make_session() as db:
#         yield db


################################################################################
# TEST
# @pt.fixture(scope="session")
# def auth():
#     return {"Authorization": config.APP_PASSWORD}
