from fastapi.responses import JSONResponse


class JSONOrForwardResponse(JSONResponse):  # pragma no cover
    def __init__(self, json_or_result):
        if hasattr(json_or_result, "status_code"):
            super().__init__(json_or_result.json(), json_or_result.status_code)
        else:
            super().__init__(json_or_result, status_code=200)
