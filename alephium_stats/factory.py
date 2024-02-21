from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from .config import config


def create_app():
    if config.FAPI_DOCS_ENABLE:
        app = FastAPI()
    else:
        app = FastAPI(openapi_url="")  # pragma: no cover

    app = _create_cors(app, config)

    return app


def _create_cors(app, config):  # pragma: no cover
    if not config.FAPI_CORS_ENABLE:
        return app

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=config.FAPI_CORS_ALLOW_CREDENTIALS,
        allow_origins=config.FAPI_CORS_ALLOW_ORIGINS,
        allow_methods=config.FAPI_CORS_ALLOW_METHODS,
        allow_headers=config.FAPI_CORS_ALLOW_HEADERS,
    )

    return app


def use_route_names_as_operation_ids(app: FastAPI) -> None:  # pragma no cover
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'
