from depends import inject  # noqa: F401
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader
from httpx import AsyncClient

from .config import config
from .exceptions import UnauthorizedUseError

# NOTE:actual no db necessary
# from depends import inject  # noqa: F401
# from sqlalchemy.orm import sessionmaker
# from .common import db_engine
# from .config import config
# from .crud import CRUD
#
# make_session = sessionmaker(db_engine, class_=CRUD, **config.DB_SESSION_CONFIG)
#
#
# async def aget_db():  # pragma: no cover
#     async with make_session() as db:
#         yield db
#
#
# DB = Depends(aget_db)
# NOTE: if fastapi is not involved
# DDB = DDepends(aget_db)


async def get_requests_async():  # pragma: no cover
    async with AsyncClient() as requests:
        yield requests


api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def validate_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header != config.FRONTEND_API_KEY:
        raise UnauthorizedUseError


Requests = Depends(get_requests_async)
ApiKey = Depends(validate_api_key)
