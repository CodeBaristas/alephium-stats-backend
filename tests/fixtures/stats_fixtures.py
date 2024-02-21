import pytest


################################################################################
# HEADER
@pytest.fixture
def header_valid_api_key():
    return {"x-api-key": "123456"}


@pytest.fixture
def header_no_valid_api_key():
    return {"x-api-key": "1234567"}


################################################################################
# REQUEST
@pytest.fixture
def req_available_address():
    return {"address": "test_address_okay123"}
