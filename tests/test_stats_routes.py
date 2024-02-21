import pytest


class TestGetBalanceAndGroup:
    @pytest.mark.asyncio
    async def test_fail_no_valid_api_key(
        self,
        client,
        header_no_valid_api_key,
        req_available_address,
    ):
        res = await client.get(
            "/stats/addresses",
            headers=header_no_valid_api_key,
            params=req_available_address,
        )
        assert res.status_code == 403
