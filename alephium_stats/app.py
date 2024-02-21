# NOTE:actual no db necessary
# from sqlalchemy.exc import SQLAlchemyError


from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from . import factory
from .common import limiter
from .exceptions import (
    BadRequestError,
    ForbiddenError,
    InternalError,
    NotFoundError,
    UnauthorizedError,
    UnauthorizedUseError,
)
from .stats.routes import router as stats_router
from .utils.alephium.exceptions import (
    AlephiumExplorerRequestError,
    AlephiumExplorerWrongAlphTypeError,
    AlephiumExplorerWrongTimeIntervalError,
    AlephiumNodeRequestError,
)
from .utils.utils import logger
from .websocket.routes import router as websocket_router

app = factory.create_app()


################################################################################
# ROUTES
factory.use_route_names_as_operation_ids(app)

app.include_router(stats_router)
app.include_router(websocket_router)

################################################################################
# RATE LIMITER
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


################################################################################
# BadRequest: 400
@app.exception_handler(AlephiumExplorerWrongAlphTypeError)
@app.exception_handler(AlephiumExplorerWrongTimeIntervalError)
@app.exception_handler(AlephiumExplorerRequestError)
@app.exception_handler(AlephiumNodeRequestError)
@app.exception_handler(ValueError)
async def handle_bad_request(_, e):
    logger.error(f"400: {e}")

    return BadRequestError(str(e))


################################################################################
# Unauthorized: 401
def handle_unauthorized(req, e):
    logger.error(f"401: {e}")

    return UnauthorizedError(str(e))


################################################################################
# Forbidden: 403
@app.exception_handler(UnauthorizedUseError)
def handle_forbidden_error(req, e):
    logger.error(f"403: {e}")

    return ForbiddenError(str(e))


################################################################################
# NotFound: 404
async def handle_not_found_error(req, e):
    logger.error(f"404: {e}")

    return NotFoundError(str(e))


################################################################################
# Internal: 500
@app.exception_handler(Exception)
async def handle_known_internal(_, e):
    logger.error(f"500: {e}")

    return InternalError(str(e))


# NOTE:actual no db necessary
# @app.exception_handler(SQLAlchemyError)
# async def handle_db_error(req, e):  # pragma: no cover
#     logger.error(f"500: DB: {e}")
#     logger.exception(e)
#
#     return InternalError("db error")


@app.exception_handler(Exception)
async def handle_internal_general_error(req, e):  # pragma: no cover
    logger.error("500: !!!!!!!!!!!!!!!!!! UNHANDLED !!!!!!!!!!!!!!!!!!")
    logger.exception(e)

    return InternalError("unknown")
