from ...exceptions import BaseError


class AlephiumNodeRequestError(BaseError):
    pass


class AlephiumExplorerRequestError(BaseError):
    pass


class AlephiumExplorerWrongTimeIntervalError(BaseError):
    pass


class AlephiumExplorerWrongAlphTypeError(BaseError):
    pass
